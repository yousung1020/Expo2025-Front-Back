from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ai.models import MotionType, UserRecording
from .models import Employee, Company
from .serializers import CompanyTokenObtainPairSerializer, EmployeeSerializer
from enrollments.models import Enrollment

class UserRecordingView(APIView):
    def get(self, request, slug, *args, **kwargs):
        # 특정 사용자의 가장 최근 평가 기록을 가져옴
        user_recording = UserRecording.objects.filter(user__emp_no=slug).order_by('-recorded_at').first()

        if not user_recording:
            return Response({"detail": "해당 사용자의 평가 기록을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        try:
            # 해당 평가와 연결된 Course의 수강 상태를 조회
            user_status = Enrollment.objects.get(
                employee__emp_no=slug, 
                course__title=user_recording.motion_type.motion_name
            ).status
        except Enrollment.DoesNotExist:
            # 수강 정보가 없을 경우를 대비해 기본값 설정
            user_status = False

        return Response({
            "ok": True,
            "user": user_recording.user.name,
            "motion_type": user_recording.motion_type.motion_name,
            "score": user_recording.score,
            "recorded_at": user_recording.recorded_at,
            "status": user_status,
        }, status=status.HTTP_200_OK)

class CompanyTokenObtainPairView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = CompanyTokenObtainPairSerializer(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            print("b")
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    직원 정보 CRUD 및 대량 등록 API
    """
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated] # 로그인한 회사만 접근 가능

    def get_queryset(self):
        # 로그인한 회사(request.user)에 소속된 직원 정보만 조회
        return Employee.objects.filter(company=self.request.user)

    def perform_create(self, serializer):
        # 직원을 새로 등록할 때, 해당 직원의 소속을 로그인한 회사로 자동 설정
        serializer.save(company=self.request.user)

    @action(detail=False, methods=["post"], url_path="bulk")
    def bulk(self, request):
        """
        직원 정보를 JSON 배열 형태로 받아 대량으로 등록/업데이트합니다.
        POST /api/organizations/employees/bulk/
        """
        
        employees_data = request.data.get("employees", [])
        if not isinstance(employees_data, list):
            return Response(
                {"error": "'employees' 필드는 리스트 형태여야 합니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        created_count = 0
        updated_count = 0

        for emp_data in employees_data:
            emp_no = emp_data.get("emp_no")
            if not emp_no:
                continue

            # update_or_create: emp_no가 존재하면 업데이트, 없으면 새로 생성
            obj, created = Employee.objects.update_or_create(
                company=request.user,
                emp_no=emp_no,
                defaults={
                    "name": emp_data.get("name", ""),
                    "dept": emp_data.get("dept", ""),
                    "phone": emp_data.get("phone", ""),
                    "email": emp_data.get("email", ""),
                },
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

            print(updated_count)

        return Response(
            {
                "message": "직원 정보 대량 처리가 완료되었습니다.",
                "created": created_count,
                "updated": updated_count,
            },
            status=status.HTTP_200_OK,
        )
