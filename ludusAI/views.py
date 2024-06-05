from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.views.generic import TemplateView
from .games.prisoners_dilemma.game import PrisonersDilemma, QLearningStrategy
import logging
import itertools

logger = logging.getLogger(__name__)

game = PrisonersDilemma()
q_learning = QLearningStrategy()

STRATEGIES = { 
    'tit_for_tat': game.tit_for_tat,
    'random': game.random_strategy,
    'always_cooperate': game.always_cooperate,
    'always_defect': game.always_defect,
}

q_learning_strategy = QLearningStrategy()
logger.info('Training Q-learning strategy...')
q_learning_strategy.train(20000, STRATEGIES['tit_for_tat'])
logger.info('Training complete.')

STRATEGIES['q_learning'] = q_learning_strategy.q_strategy

def index(request):
    return render(request, 'index.html')

class PlayPrisonersDilemma(APIView):
    def get(self, request, format=None):
        # strategy1_name = request.query_params.get('strategy1')
        # strategy2_name = request.query_params.get('strategy2')
        # rounds = int(request.query_params.get('rounds', 100))
        rounds = 10
        
        strategy1 = STRATEGIES['q_learning']
        strategy2 = STRATEGIES['tit_for_tat']
        score1, score2, history1, history2 = game.play(strategy1, strategy2, rounds)
        return Response({
            'score1': score1,
            'score2': score2,
            'history': self.formatted_history(history1, history2)
        })

    def formatted_history(self, history1, history2): 
        array = list(itertools.chain.from_iterable(zip(history1, history2)))

        turns = []
        for i in range(0, len(array), 2):
            turns.append(f"Player 1: {array[i]}" + "   |   " + f"Player 2: {array[i+1]}")

        return turns
    
# class PlayPrisonersDilemma(APIView):
#     def get(self, request, format=None):
#         # Your logic here
#         return Response({"message": "Hello from Django DRF!"})