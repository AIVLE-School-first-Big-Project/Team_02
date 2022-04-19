from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from datetime import datetime


class UserManager(BaseUserManager):
    def create_user(self, username, name, email, password=None):
        if not username:
            raise ValueError("아이디를 입력해주세요.")
        if not name:
            raise ValueError("이름을 입력해주세요.")
        if not email:
            raise ValueError("이메일을 입력해주세요.")
        
        user = self.model(
            username = username,
            name = name,
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name, email, password):
        user = self.create_user(
            username = username,
            name = name,
            email = self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser):
    
    username = models.CharField(unique=True, max_length=150, blank=True)
    name = models.CharField(max_length=128)
    email = models.EmailField(max_length=128, unique=True)
    date_joined = models.DateField(default=datetime.now)
    is_staff = models.IntegerField(blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()  # 회원가입을 다룰 클래스를 지정한다.

    USERNAME_FIELD = 'username'   # 식별자로 사용할 필드.
    REQUIRED_FIELDS = ['name', 'email']            # 회원가입 때 필수 입력필드.
    
    # 권한 소지여부를 판단하기 위한 메서드
    def has_perm(self, perm, obj=None):
        return True
    
    # 앱 라벨을 받아, 해당 앱에 접근 가능한지 파악
    def has_module_perms(self, app_label):
        return True
    
    # 관리자화면에 접근
    @property
    def is_staff(self):
        return self.is_admin