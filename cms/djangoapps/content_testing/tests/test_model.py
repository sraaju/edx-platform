"""
Unit tests on the models that make up automated content testing
"""

from textwrap import dedent
from django.test import TestCase
from xmodule.modulestore import Location
from xmodule.modulestore.tests.factories import CourseFactory, ItemFactory
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.django import modulestore
from content_testing.models import ContentTest, Response, Input
from capa.tests.response_xml_factory import CustomResponseXMLFactory
import pickle


class ContentTestTest(ModuleStoreTestCase):
    '''set up a content test to test'''

    SCRIPT = dedent("""
    def is_prime (n):
        primality = True
        for i in range(2,int(math.sqrt(n))+1):
            if n%i == 0:
                primality = False
                break
        return primality

    def test_prime(expect,ans):
        a1=int(ans[0])
        return is_prime(a1)""").strip()
    NUM_INPUTS = 2  # tied to script

    HTML_SUMMARY = dedent("""
    <table>
        <tr>
            <td>
                Inputs:
            </td>
            <td>
                Should Be:
            </td>
            <td>
                Verdict:
            </td>
        </tr>
        <tr>
            <td>
                <ol>
                    <li> 5 </li>
                    <li> 174440041 </li>
                </ol>
            </td>
            <td>
                Correct
            </td>
            <td>
                Not Run
            </td>
        <tr>
    </table>""").strip()

    HTML_FORM = """<div><p/><span><section id="inputtype_i4x-MITx-999-problem-Problem_4_2_1" class=" capa_inputtype "><div class="unanswered " id="status_i4x-MITx-999-problem-Problem_4_2_1"><input type="text" name="input_i4x-MITx-999-problem-Problem_4_2_1" id="input_i4x-MITx-999-problem-Problem_4_2_1" value = "5" aria-describedby="answer_i4x-MITx-999-problem-Problem_4_2_1" /><p class="status" aria-describedby="input_i4x-MITx-999-problem-Problem_4_2_1">\n        unanswered\n      </p><p id="answer_i4x-MITx-999-problem-Problem_4_2_1" class="answer"/></div></section><section id="inputtype_i4x-MITx-999-problem-Problem_4_2_2" class=" capa_inputtype "><div class="unanswered " id="status_i4x-MITx-999-problem-Problem_4_2_2"><input type="text" name="input_i4x-MITx-999-problem-Problem_4_2_2" id="input_i4x-MITx-999-problem-Problem_4_2_2" value = "174440041" aria-describedby="answer_i4x-MITx-999-problem-Problem_4_2_2" /><p class="status" aria-describedby="input_i4x-MITx-999-problem-Problem_4_2_2">\n        unanswered\n      </p><p id="answer_i4x-MITx-999-problem-Problem_4_2_2" class="answer"/></div></section></span></div><br/>\n  This Should be marked as:\n  Correct: <input type="radio" name="should_be" value="Correct" id="correct_box" checked="True">\n  Incorrect: <input type="radio" name="should_be" value="Incorrect" id="incorrect_box" >\n  Error: <input type="radio" name="should_be" value="ERROR" id="incorrect_box" >\n<br>"""

    VERDICT_PASS = "Pass"
    VERDICT_FAIL = "Fail"
    VERDICT_ERROR = "ERROR"
    VERDICT_NONE = "Not Run"

    def setUp(self):
        #course in which to put the problem
        self.course = CourseFactory.create()
        assert self.course

        #make the problem
        custom_template = "i4x://edx/templates/problem/Custom_Python-Evaluated_Input"

        #change the script if 1
        problem_xml = CustomResponseXMLFactory().build_xml(
            script=self.SCRIPT,
            cfn='test_prime',
            num_inputs=self.NUM_INPUTS)

        self.problem = ItemFactory.create(
            parent_location=self.course.location,
            data=problem_xml,
            template=custom_template,
            num_inputs=self.NUM_INPUTS)

        #sigh
        input_id_base = self.problem.id.replace('://', '-').replace('/', '-')

        # saved responses for making tests
        self.response_dict_correct = {
            input_id_base + '_2_1': '5',
            input_id_base + '_2_2': '174440041'
        }
        self.response_dict_incorrect = {
            input_id_base + '_2_1': '4',
            input_id_base + '_2_2': '541098'
        }

        self.response_dict_error = {
            'anyone lived': 'in a pretty how town'
        }
        assert self.problem

        # Make a collection of ContentTests to test
        self.pass_correct = ContentTest.objects.create(
            problem_location=self.problem.location,
            should_be='Correct',
            response_dict=self.response_dict_correct
        )

        self.pass_incorrect = ContentTest.objects.create(
            problem_location=self.problem.location,
            should_be='Incorrect',
            response_dict=self.response_dict_incorrect
        )

        self.fail_correct = ContentTest.objects.create(
            problem_location=self.problem.location,
            should_be='Incorrect',
            response_dict=self.response_dict_correct
        )

        self.fail_incorrect = ContentTest.objects.create(
            problem_location=self.problem.location,
            should_be='Correct',
            response_dict=self.response_dict_incorrect
        )

        self.fail_error = ContentTest.objects.create(
            problem_location=self.problem.location,
            should_be='Correct',
            response_dict=self.response_dict_error
        )

        self.pass_error = ContentTest.objects.create(
            problem_location=self.problem.location,
            should_be="ERROR",
            response_dict=self.response_dict_error)


class WhiteBoxTests(ContentTestTest):
    '''test that inner methods are working'''

    def test_make_capa(self):
        '''test that the capa instantiation happens properly'''
        test_model = ContentTest.objects.create(
            problem_location=self.problem.location,
            should_be='Correct')

        capa = test_model.capa_problem

        #assert no error
        assert self.SCRIPT in capa.problem_text

    def test_create_children(self):
        '''test that the ContentTest is created with the right structure'''

        # import nose; nose.tools.set_trace()
        test_model = ContentTest.objects.create(
            problem_location=str(self.problem.location),
            should_be='Correct')

        #check that the response created properly
        response_set = test_model.response_set
        self.assertEqual(response_set.count(), 1)

        #and the input
        input_set = response_set.all()[0].input_set
        self.assertEqual(input_set.count(), self.NUM_INPUTS)

    def test_create_dictionary(self):
        '''tests the constructions of the response dictionary'''
        test_model = ContentTest.objects.create(
            problem_location=self.problem.location,
            should_be='Correct',
            response_dict=self.response_dict_correct
        )
        # test_model._create_children()

        created_dict = test_model._get_response_dictionary()

        self.assertEqual(self.response_dict_correct, created_dict)

    def test_update_dict(self):
        '''tests the internal functionality of updating the dictionary through the children'''
        test_model = self.pass_correct

        # update the dictionary with wrong answers
        test_model._update_dictionary(self.response_dict_incorrect)

        # update the attribute too
        test_model.response_dict = self.response_dict_incorrect

        # make sure they match
        self.assertEqual(test_model._get_response_dictionary(), test_model._get_dict_from_children())


class BlackBoxTests(ContentTestTest):
    '''test overall behavior of the ContentTest model'''

    def test_pass_correct(self):
        '''test that it passes with correct answers when it should'''

        # run the test
        self.pass_correct.run()

        # make sure it passed
        self.assertEqual(self.VERDICT_PASS, self.pass_correct.verdict)

    def test_fail_incorrect(self):
        '''test that it fails with incorrect answers'''

        # run the testcase
        self.fail_incorrect.run()

        # make sure it failed
        self.assertEqual(self.VERDICT_FAIL, self.fail_incorrect.verdict)

    def test_pass_incorrect(self):
        '''test that it passes with incorrect'''

        # run the test
        self.pass_incorrect.run()

        # make sure it passed
        self.assertEqual(self.VERDICT_PASS, self.pass_incorrect.verdict)

    def test_fail_correct(self):
        '''test that it fails with incorrect answers'''

        # run the testcase
        self.fail_incorrect.run()

        # make sure it failed
        self.assertEqual(self.VERDICT_FAIL, self.fail_incorrect.verdict)

    def test_pass_error(self):
        """
        test that we get a pass when it expects and gets an error
        """

        # run the testcae
        self.pass_error.run()

        # make sure it passed
        self.assertEqual(self.VERDICT_PASS, self.pass_error.verdict)

    def test_fail_error(self):
        """
        Test that a badly formatted dictionary results in error
        """

        test_model = self.fail_error
        test_model.run()

        self.assertEqual(self.VERDICT_ERROR, test_model.verdict)

    def test_reset_verdict(self):
        '''test that changing things resets the verdict'''

        test_model = self.pass_correct

        # run the testcase (generates verdict)
        test_model.run()

        # update test
        test_model.response_dict = self.response_dict_incorrect
        test_model.save()

        #ensure that verdict is now null
        self.assertEqual(self.VERDICT_NONE, test_model.verdict)

    def test_change_dict(self):
        '''test that the verdict changes with the new dictionary on new run'''

        test_model = self.pass_correct

        # update test
        test_model.response_dict = self.response_dict_incorrect
        test_model.save()

        # run the test
        test_model.run()

        # assert that the verdict is now self.VERDICT_FAIL
        self.assertEqual(self.VERDICT_FAIL, test_model.verdict)

    def test_nochange_dict(self):
        """
        test that updating the dictionary without changing it doesn't break anything
        """
        test_model = self.pass_correct
        test_model.response_dict = self.response_dict_correct
        test_model.save()

        # get fresh from db
        new_model = ContentTest.objects.get(pk=test_model.pk)

        self.assertEqual(pickle.loads(new_model.response_dict), self.response_dict_correct)

    # def test_get_html_summary(self):
    #     """
    #     test that html is rendered correctly
    #     """

    #     html = self.pass_correct.get_html_summary()
    #     self.assertEqual(html, self.HTML_SUMMARY)

    # def test_get_html_form(self):
    #     """
    #     test that html is rendered correctly
    #     """

    #     html = self.pass_correct.get_html_form()

    #     self.assertEqual(html, self.HTML_FORM)

