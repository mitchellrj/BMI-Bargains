from copy import deepcopy
import datetime
from email.message import Message
import threading
import time

from repoze.sendmail.delivery import DirectMailDelivery
from repoze.sendmail.mailer import SMTPMailer
import transaction

import config
from search import performSearch

class SearchQueue(threading.Thread):
    def __init__(self, root, *args, **kwargs):
        super(SearchQueue, self).__init__(*args, **kwargs)
        self.root = root
        self.daemon = True

    def run(self):
        other_threads = threading.enumerate()
        other_threads.remove(threading.current_thread())
        if self.name in [t.name for t in other_threads]:
            return
        mailer = SMTPMailer(port=config.SMTP_PORT)
        delivery = DirectMailDelivery(mailer)
        a = True
        while True:
            items = deepcopy(self.root)
            for hash, search in items.iteritems():
                if not search['active']:
                    continue
                results = performSearch(self.root, search)
                tell = []
                for result in results:
                    key = result.copy()
                    del key['total_price']
                    del key['book_link']
                    if key not in search['told']:
                        tell.append(result)
                        search['told'].append(key)

                if not tell:
                    continue

                url = config.URL
                remove_link = '%s/remove?email=%s&code=%s' % (url, search['email'], hash)
                journies = []
                for result in tell:
                    journey = config.JOURNEY_STR % result
                    journies.append(journey)

                journies = config.JOURNEY_JOINER.join(journies)

                message_text = config.EMAIL_MATCHES % {'journies': journies,
                                                       'remove_link': remove_link}

                message = Message()
                message.set_payload(message_text)
                delivery.send(config.FROM_ADDR, [search['email'],], message)
                transaction.commit()
            time.sleep(20)
