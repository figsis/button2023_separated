# from project._builtin import Page, WaitPage
from ._builtin import Page, WaitPage
from .models import Constants
from otree.api import *
from .models import Player


def vars_for_all_templates(self):
    return {
        'treatment': self.session.vars["treatment"],
        'selected':  self.session.vars["selected"]}


class SummaryTask1_(Page):
    def is_displayed(self):
        player = self.player
        return player.treatment == "ButtonA" or player.treatment == "ButtonB"


class SummaryTask1_danat(Page):
    def is_displayed(self):
        player = self.player
        return player.treatment == "NoButton"

class Instructions_Attention(Page):
    pass

class Button(Page):
    form_model = 'player'
    form_fields = ['button', 'store_time']
    timeout_seconds = Constants.timer

    def is_displayed(self):
        player = self.player
        return player.treatment == "ButtonA" or player.treatment == "ButtonB"

#class ButtonClicked(Page):
    #   form_model = 'player'

        #  def get_timeout_seconds(self):
    #      return self.player.store_time

        #  def is_displayed(self):
        #      player = self.player
#      return player.treatment == "ButtonA" and player.button==1 or player.treatment == "ButtonB" and player.button==1


#class danat_clicked(Page):
    #   form_model = 'player'
    #form_fields = ['danat']

    #def get_timeout_seconds(self):
    #   return self.player.store_time

    ##def is_displayed(self):
        #  player = self.player
        #return player.treatment == "NoButton"







class task_timed(Page):
    form_model = 'player'
    form_fields = ['danat','store_time']
    timeout_seconds = Constants.timer


    def is_displayed(self):
        player = self.player
        return player.treatment == "NoButton"


class Payment(Page):
    form_model = 'player'
    form_fields = [ 'bonus', 'payoff2_self', 'payoff2_charity', 'payoff2_self_danat',
                    'payoff2_charity_danat', 'payoff3']
    def vars_for_template(self):
        return dict(
            payoff_svo=self.player.participant.vars["payoff_svo"],
            payoff_svo_other=self.player.participant.vars["payoff_svo_other"],
            #payoff2_charity=self.player.participant.vars["payoff2_charity"],
            payoff2_charity=self.player.payoff2_charity,
            payoff2_charity_danat=self.player.payoff2_charity_danat,
            #paid_slider = self.player.participant.vars["paid_slider"],
            selected=self.player.selected,
            payoff2_self=self.player.payoff2_self,
            payoff2_self_danat=self.player.payoff2_self_danat,
            bonus= self.player.bonus,
            payoff3= self.player.payoff3,
            payoff4 = self.player.payoff4

        )


class Attention_Survey(Page):
    form_model = 'player'
    form_fields = ['q_number']

    def vars_for_template(self):
        return dict(q_number=self.player.q_number)

class Survey(Page):
    form_model = 'player'
    form_fields = []

    def vars_for_template(self):
        return dict(payoff1_self=self.player.participant.vars["payoff1_self"],
                    payoff2_self=self.participant.vars["payoff2_self"],
                    store_time = self.player.store_time)

    def is_displayed(self):
        player = self.player
        return player.treatment == "ButtonA" or player.treatment == "ButtonB"

    def get_form_fields(self):
        if self.player.treatment == "ButtonA":
            #selfish button pressed but altruistic dana (altruistic-selfish)
            if self.player.store_time != 0 and self.participant.vars["payoff1_self"]  == 5:
                return ['q0', 'q1','q_change']
            #selfish button pressed and selfish dana (selfish-selfish)
            elif self.player.store_time != 0 and self.participant.vars["payoff1_self"]  ==10:
                return ['q0','q1','q_nochange']
            # selfish button not pressed and selfish dana (selfish-altruistic)
            elif self.player.store_time == 0 and self.participant.vars["payoff1_self"]  ==10:
                return ['q0','q2','q_change']
            # selfish button not pressed and altruistic dana (altruistic-altruistic)
            elif self.player.store_time == 0 and self.participant.vars["payoff1_self"] == 5:
                return ['q0','q2','q_nochange']
        if self.player.treatment == "ButtonB":
            #altruistic button pressed and altruistic dana (altruistic-altruistic)
            if self.player.store_time != 0 and self.participant.vars["payoff1_self"]  == 5:
                return ['q0', 'q1',  'q_nochange']
            #altruistic button pressed and selfish dana (selfish-altruistic)
            elif self.player.store_time != 0 and self.participant.vars["payoff1_self"]  ==10:
                return ['q0', 'q1', 'q_change']
            #altruistic button not pressed and selfish dana (selfish-selfish)
            elif self.player.store_time == 0 and self.participant.vars["payoff1_self"]  ==10:
                return ['q0', 'q2',  'q_nochange']
            # altruistic button not pressed and altruistic dana (altruistic-selfish)
            elif self.player.store_time == 0 and self.participant.vars["payoff1_self"] == 5:
                return ['q0', 'q2',  'q_change']

    def before_next_page(self):
        self.player.set_payoffs()
        self.player.set_bonus()
        self.player.set_payoff3()


class Survey_danat(Page):
    form_model = 'player'
    form_fields = []

    def vars_for_template(self):
        return dict(payoff1_self=self.player.participant.vars["payoff1_self"],
                    payoff2_self_danat=self.participant.vars["payoff2_self_danat"])

    def get_form_fields(self):
        if self.participant.vars["payoff1_self"] ==  self.participant.vars["payoff2_self_danat"]:
            return ['q_nochange']
        elif self.participant.vars["payoff1_self"] != self.participant.vars["payoff2_self_danat"]:
            return ['q_change']


    def is_displayed(self):
        player = self.player
        return player.treatment == "NoButton"

    def before_next_page(self):
        self.player.set_payoffs()
        self.player.set_bonus()
        self.player.set_payoffsdanat()

class Comments(Page):
    form_model = 'player'
    form_fields = ['q_feedback', 'q_feedback_pilot']

#class PaymentSelected(Page):
    #    form_model = 'player'

    #def vars_for_template(self):
        #   try:
        #   if self.player.participant.vars["payoff2_charity"] == 0:
        #       payoff2_charity_neg = False
        #   elif self.player.participant.vars["payoff2_charity"][:1] == "-":
        #       payoff2_charity_neg = True
        #   else:
        #       payoff2_charity_neg = False
        #except TypeError:
        #   payoff2_charity_neg = False
        #   print('typerror, but ', self.player.participant.vars["payoff2_charity"], ' = payoff2_charity')
        #return dict(
        #   payoff1_self=self.player.participant.vars["payoff1_self"],
        #   payoff1_charity=self.player.participant.vars["payoff1_charity"],
        #   payoff2_self=self.player.participant.vars["payoff2_self"],
        #   payoff2_charity=self.player.participant.vars["payoff2_charity"],
        #   payoff2_charity_neg=payoff2_charity_neg,
        #   selected=self.player.selected,
        #   punished=self.player.punished,
        #   punishment=self.player.punishment,
#   button=self.player.button)


#class BackToProlific(Page):
    #   form_model = 'player'

    #def dispatch(self, request, *args, **kwargs):
        #   if request.method == 'GET':
        #   address = "https://app.prolific.co/submissions/complete?cc=52C82836"
        #   return HttpResponseRedirect(address)
        #return super(Page, self).dispatch(request, *args, **kwargs)


page_sequence = [SummaryTask1_,
                 SummaryTask1_danat,
                 Instructions_Attention,
                 Button,
                 #ButtonClicked,
                 task_timed,
                 #danat_clicked,
                 Attention_Survey,
                 Survey,
                 Survey_danat,
                 Comments,
                 Payment
                 ]
