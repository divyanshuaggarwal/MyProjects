# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from pytz import country_timezones, timezone


def find_city(query):
    for country, cities in country_timezones.items():
        for city in cities:
            if query in city:
                yield timezone(city)

def find_timezone(city):
    for tz in find_city(city.title()):
        return str(tz)

class ActionShowTimeZone(Action):

    def name(self) -> Text:
        return "action_show_time_zone"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = tracker.get_slot("city")
        timezone = find_timezone(str(city))
        if timezone is None:
            output = "Could not find the time zone of {}".format(city)
        else:
            output = "Time zone of {} is {}".format(city, timezone)
        dispatcher.utter_message(text=output)

        return []


