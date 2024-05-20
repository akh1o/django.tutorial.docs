from django.test import TestCase
import datetime
from .models import Question, Choice
from django.utils import timezone
from django.urls import reverse

# Create your tests here.
class QuestionModelTests(TestCase):
	def test_was_published_recently_with_future_question(self):
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		self.assertIs(future_question.was_published_recently(), False)

	def test_was_published_recently_with_recent_question(self):
		time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
		recent_question = Question(pub_date=time)
		self.assertIs(recent_question.was_published_recently(), True)

	def test_was_published_recently_with_old_question(self):
		time = timezone.now() - datetime.timedelta(days=1, seconds=1)
		old_question = Question(pub_date=time)
		self.assertIs(old_question.was_published_recently(), False)

def create_question(question_text, days=0):
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
	def test_no_questions(self):
		response = self.client.get(reverse("polls:index"))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are available.")
		self.assertQuerySetEqual(response.context["latest_question_list"], [])

	def test_past_question(self):
		question = create_question(question_text="Past Question", days=-30)
		response = self.client.get(reverse("polls:index"))
		self.assertQuerySetEqual(response.context["latest_question_list"], [question])

	def test_future_question(self):
		question = create_question(question_text="future_question", days=30)
		response = self.client.get(reverse("polls:index"))
		self.assertQuerySetEqual(response.context["latest_question_list"], [])
		self.assertContains(response, "No polls are available.")

	def test_future_and_past_questions(self):
		future_question = create_question(question_text="Future Question", days=30)
		past_question = create_question(question_text="Past Question", days=-30)
		response = self.client.get(reverse("polls:index"))
		self.assertQuerySetEqual(response.context["latest_question_list"], [past_question])

	def test_two_past_question(self):
		question1 = create_question(question_text="past question1", days=-30)
		question2 = create_question(question_text="past question2", days=-30)
		response = self.client.get(reverse("polls:index"))
		self.assertQuerySetEqual(response.context["latest_question_list"], [question2, question1])

class QuestionDetailViewTests(TestCase):
	def test_future_question(self):
		question = create_question(question_text="future question", days=30)
		response = self.client.get(reverse("polls:detail", args=[question.id,]))
		self.assertEqual(response.status_code, 404)

	def test_past_question(self):
		question = create_question(question_text="past question", days=-30)
		response = self.client.get(reverse("polls:detail", args=[question.id,]))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, question.question_text)

def create_question_with_choice(question_text, choice_text):
	question = create_question(question_text=question_text)
	choice = Choice.objects.create(question=question, choice_text=choice_text)
	return question






