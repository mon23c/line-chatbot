from linebot.models import TextSendMessage, ImageSendMessage
from function import learn, stalk, learn_data
import csv, re, random, urllib.request, urllib.parse, unittest

class TestingData(unittest.TestCase):
    def test_learn(self):
    	expected = TextSendMessage("Words 'berantem yuks' has learned")
    	result = learn("berantem yuks","Ayo! Saya tidak suka ketenangan")
    	self.assertEqual(expected, result)
    def test_stalk(self):
        expected = TextSendMessage("Photo doesn't exist. Perhaps this user account private or don't have any photos yet")
        result = stalk("mett2n")
        self.assertEqual(expected, result)

if __name__ == "__main__":
	unittest.main()