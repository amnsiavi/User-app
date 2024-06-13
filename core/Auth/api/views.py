from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR,HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError

from django.contrib.auth.models import User
from Auth.api.serializers import AuthSerializer
from Auth.permissions import AdminUser, RegularUser



@api_view(["GET"])
@permission_classes([AdminUser|RegularUser,IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_all_users(requests):
    try:
        users = User.objects.all()
        seriliazer = AuthSerializer(users,many=True)
        return Response({
        'data':seriliazer.data,
        'msg':'Fetch SucessFul'
        },status=HTTP_200_OK)
    except Exception as e:
        return Response({
            'errors':str(e),
            'status_code': HTTP_500_INTERNAL_SERVER_ERROR
        })
    
@api_view(['POST'])
@permission_classes([AdminUser,IsAuthenticated])
@authentication_classes([JWTAuthentication])
def create_user(request):
    
    try:
        serializer = AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'data':serializer.data,
           'msg':'User Created'
        },status=HTTP_200_OK)

    except TokenError as te:
        return Response({
            'errors':str(te),
            'msg':'Token Expired or Invalid'
        },status=HTTP_401_UNAUTHORIZED)
    except ValidationError as ve:
        return Response({
            'errors':ve.detail,
            'status_code':HTTP_400_BAD_REQUEST

        })
    except Exception as e:
        return Response({
            'errors':str(e),
            'status_code':HTTP_500_INTERNAL_SERVER_ERROR
        })


@api_view(['GET','DELETE', 'PUT','PATCH'])
@permission_classes([AdminUser|RegularUser,IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_user(request,pk):
    
    try:
        if request.method == 'GET':
            instance = User.objects.get(pk=pk)
            serializer = AuthSerializer(instance)
            return Response({
            'data':serializer.data,
            'msg':'User Fetched',
            'user':str(request.user)
            },status=HTTP_200_OK)
        
        elif request.method == 'DELETE':
            
            try:
                username = request.user
                user = User.objects.filter(username=username).first()
                if user.is_superuser:
                    instance = User.objects.get(pk=pk)
                    instance.delete()
                    return Response({
                        'msg':'User Deleted Sucessfully'
                    },status=HTTP_200_OK)
                else:
                    return Response({
                        'msg':'User not allowed',
                        'status_code':HTTP_401_UNAUTHORIZED
                    })

            except TokenError as te:
                return Response({
                    'errors':str(te),
                    'msg':'Token Expired',
                    'status_code': HTTP_401_UNAUTHORIZED
                })
          
        elif request.method == 'PUT':

            try:
                username = request.user
                user = User.objects.filter(username=username).first()
                if user.is_superuser:
                    if len(request.data) == 0:
                        return Response({
                            'errors':'Recieved Empty Object',
                            'status_code':HTTP_400_BAD_REQUEST
                        })
                    serializer = AuthSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({
                            'msg':'User Updated'
                        },status=HTTP_200_OK)
                    else:
                        return Response({
                            'errors':'Recieved Invalid Object',
                            'status_code':HTTP_400_BAD_REQUEST
                        })
                    
                else:
                    return Response({
                        'errors':'User not allowed',
                        'status_code':HTTP_401_UNAUTHORIZED
                    })
            except TokenError as te:
                return Response({
                    'errors':str(te),
                    'msg':'Token Expired',
                    'status_code':HTTP_401_UNAUTHORIZED
                })
           
        elif request.method == 'PATCH':

            try:
                username = request.user
                user = User.objects.filter(username=username).first()
                if user.is_superuser:
                    if len(request.data) == 0:
                        return Response({
                            'errors':'Recieved Empty Objects',
                            'status_code':HTTP_400_BAD_REQUEST
                        })
                    serializer = AuthSerializer(data=request.data,partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({
                            'data':serializer.data,
                            'msg':'User Updated'
                        },status=HTTP_200_OK)
                    else:
                        return Response({
                            'errors':'Recieved Invalid Object',
                            'status_code':HTTP_400_BAD_REQUEST
                        })
                else:
                    return Response({
                        'errors':'User not allowed',
                        'status_code':HTTP_401_UNAUTHORIZED
                    })
            
            except TokenError as te:
                return Response({
                    'errors':str(te),
                    'msg':'Token Expired'
                })
            
          
        else:
            return Response({
                'errors':'Method Not Allowed'
            })
            

    except Exception as e:
        return Response({
            'errors':str(e),
            'status_code':HTTP_500_INTERNAL_SERVER_ERROR
        })