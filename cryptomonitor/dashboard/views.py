from django.shortcuts import render
import argparse
import sys
from .utilities import data_retrieval
import json

# Create your views here.
def index(request):

    historic_price = data_retrieval.get_historic_price()
    engine = data_retrieval.open_db()
    data_retrieval.get_live_price(engine)
    df = pd.read_sql('MATICUSDT',engine)
    print("here ", df[-1])
    context = {"closes" : json.dumps(list(historic_price.Close.astype(int))),
            "dates" : json.dumps(list(historic_price.index.astype(str))),
            "volume" : json.dumps(list(historic_price.Volume.astype(int)))

        
    }

    return render(request, 'index.html', context)