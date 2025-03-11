from django.shortcuts import render
import stripe
import os
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Subscription, Plan
from .serializers import PlanSerializer, SubscriptionSerializer, CreateCheckoutSessionSerializer
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model
from .models import Plan

User = get_user_model()

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

class CreateCheckoutSessionView(APIView):
    @swagger_auto_schema(request_body=CreateCheckoutSessionSerializer)
    def post(self, request, *args, **kwargs):
        plan_id = request.data.get('plan_id')
        user_email = request.user.email
        try:
            plan = Plan.objects.get(id=plan_id)
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': plan.stripe_plan_id,
                    'quantity': 1,
                }],
                mode='subscription',
                customer_email=user_email,
                success_url=request.build_absolute_uri('/success/?session_id={CHECKOUT_SESSION_ID}'),  # Replace with your success URL
                cancel_url=request.build_absolute_uri('/cancel/'),   # Replace with your cancel URL
            )
            return Response({'payment_url': checkout_session.url}, status=status.HTTP_200_OK)
        
        except Plan.DoesNotExist:
            return Response({'error': 'Invalid plan ID'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.environ.get('STRIPE_WEBHOOK_SECRET')
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    # Handle the event when checkout session completes
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        user_email = session.get('customer_email')  # Get customer email
        subscription_id = session.get('subscription')  # Get subscription ID from Stripe
        if not subscription_id:
            return HttpResponse(status=400)  # Subscription ID is required
        
        # Fetch the Stripe subscription details
        stripe_subscription = stripe.Subscription.retrieve(subscription_id)

        # Get the price ID from the subscription
        price_id = stripe_subscription['items']['data'][0]['price']['id']

        # Retrieve the corresponding Plan from the database
        try:
            user = User.objects.get(email=user_email)
            plan = Plan.objects.get(stripe_plan_id=price_id)
        except User.DoesNotExist:
            return HttpResponse(status=400)  # User not found
        except Plan.DoesNotExist:
            return HttpResponse(status=400)  # Plan not found

        # Calculate subscription end date based on plan duration
        start_date = timezone.now()
        if plan.duration == "1 week":
            end_date = start_date + timedelta(days=7)
        elif plan.duration == "1 month":
            end_date = start_date + timedelta(days=30)
        elif plan.duration == "1 year":
            end_date = start_date + timedelta(days=365)
        else:
            end_date = start_date  # Default to start_date if duration is unknown

        # Store subscription details in the database
        Subscription.objects.create(
            user=user,
            plan=plan,
            stripe_subscription_id=subscription_id,
            status='active',
            start_date=start_date,
            end_date=end_date
        )

    return HttpResponse(status=200)





class PlanViewSet(ReadOnlyModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    





class SubscriptionViewSet(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)