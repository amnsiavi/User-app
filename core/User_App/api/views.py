from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from Auth.permissions import AdminUser, RegularUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from User_App.models import UserAppModel
from User_App.api.serializer import UserAppSerializer



@api_view(['GET'])
@permission_classes([AdminUser|RegularUser,IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_app_users(request):

    try:
        instance = UserAppModel.objects.all()
        seriliazer = UserAppSerializer(instance,many=True)
        return Response({
            'data':seriliazer.data
        },status=HTTP_200_OK)
    except TokenError as te:
        return Response({
            'errors':str(e),
            'msg':'Token Expired or Invlid Format'
        })
    except ValidationError as ve:
        return Response({
            'errors':ve.detail,
            'msg':'Invalid Object Recieved',
            'status_code':HTTP_401_UNAUTHORIZED
        })
    except Exception as e:
        return Response({
            'error':'Server Error',
            'msg':str(e),
            'status_code':HTTP_500_INTERNAL_SERVER_ERROR
        })


@api_view(['POST'])
@permission_classes([AdminUser,IsAuthenticated])
@authentication_classes([JWTAuthentication])
def create_app_users(request):
    
    try:
        if len(request.data) == 0:
            return Response({
                'errors':'Recieved Empty Objects',
                'status_code':HTTP_400_BAD_REQUEST
            })
        serializer = UserAppSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'data':serializer.data,
            'msg':'Reccord Created'
        },status=HTTP_200_OK)

    except TokenError as te:
        return Response({
            'msg':'Token Expired or Invalid Format',
            'errors':str(te),
            'status_code':HTTP_401_UNAUTHORIZED
        })
    except ValidationError as ve:
        return Response({
            'errors':ve.detail,
            'status_code':HTTP_400_BAD_REQUEST
        })
    except Exception as e:
        return Response({
            'errors':str(e),
            'status_code': HTTP_500_INTERNAL_SERVER_ERROR
        })