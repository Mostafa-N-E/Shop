from django.test import TestCase
from django.urls import reverse

from order.models import BaseOrder, Order


def create_order(customer):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    # time = timezone.now() + datetime.timedelta(days=days)
    base_order = BaseOrder(customer=customer)
    return Order.objects.create(order_base=base_order)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        # question = create_question(question_text="Past question.", days=-30)
        question = create_order(customer=self.client)

        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )


