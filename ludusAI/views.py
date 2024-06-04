from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import TemplateView
from .games.prisoners_dilemma.game import PrisonersDilemma, QLearningStrategy

q_learning_strategy = QLearningStrategy()
q_learning_strategy.train(1000, q_learning_strategy.q_strategy)

class PlayPrisonersDilemma(APIView):
    def get(self, request, format=None):
        strategy1_name = request.query_params.get('strategy1')
        strategy2_name = request.query_params.get('strategy2')
        rounds = int(request.query_params.get('rounds', 100))
        game = PrisonersDilemma()
        q_learning = QLearningStrategy()
        strategies = {
            'tit_for_tat': game.tit_for_tat,
            'always_cooperate': game.always_cooperate,
            'always_defect': game.always_defect,
            'q_learning': q_learning_strategy,
        }
        strategy1 = strategies[strategy1_name]
        strategy2 = strategies[strategy2_name]
        score1, score2, history1, history2 = game.play(strategy1, strategy2, rounds)
        return Response({
            'score1': score1,
            'score2': score2,
            'history1': history1,
            'history2': history2
        })
    
class PlayPrisonersDilemma(APIView):
    def get(self, request, format=None):
        # Your logic here
        return Response({"message": "Hello from Django DRF!"})