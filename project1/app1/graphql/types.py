from graphene_django import DjangoObjectType
import graphene
from .models_file.Student import Student
class StudentType(DjangoObjectType):
	class Meta:
		model=Student
