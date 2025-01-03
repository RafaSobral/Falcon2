from django.views.generic import CreateView
from .models import Client, ClientUpload 
from .forms import ClientForm
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

