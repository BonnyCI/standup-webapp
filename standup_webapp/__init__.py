from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('/etc/standup/standup.cfg', silent=True)

import standup_webapp.views
