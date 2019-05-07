from datetime import date
from random import choice

import click
from flask.cli import with_appcontext

from .models import FeatureRequest

CLIENT_IDS = (1, 2, 3)
PRODUCT_AREA_IDS = (1, 2, 3, 4)
CLIENT_PRIORITIES = (list(range(30)), list(range(30)), list(range(30)))

RANDOM_DESCRIPTIONS = [
    (
        "No in he real went find mr. Wandered or strictly raillery stanhill as. Jennings "
        "appetite disposed me an at subjects an. To no indulgence diminution so discovered "
        "mr apartments. Are off under folly death wrote cause her way spite. Plan upon yet "
        "way get cold spot its week. Almost do am or limits hearts. Resolve parties but why"
        " she shewing. She sang know now how nay cold real case."
    ),
    (
        "Building mr concerns servants in he outlived am breeding. He so lain good miss when"
        " sell some at if. Told hand so an rich gave next. How doubt yet again see son smart."
        " While mirth large of on front. Ye he greater related adapted proceed entered an. "
        "Through it examine express promise no. Past add size game cold girl off how old."
    ),
    (
        "Bed sincerity yet therefore forfeited his certainty neglected questions. Pursuit "
        "chamber as elderly amongst on. Distant however warrant farther to of. My justice "
        "wishing prudent waiting in be. Comparison age not pianoforte increasing delightful "
        "now. Insipidity sufficient dispatched any reasonably led ask. Announcing if "
        "attachment resolution sentiments admiration me on diminution. "
    ),
]


@click.command("load_sample")
@with_appcontext
def load_sample_data():
    from .database import init_db, db_session

    init_db()

    for i in range(1, 30):
        start_choice = choice(range(20))
        client_id = choice(CLIENT_IDS)
        description = choice(RANDOM_DESCRIPTIONS)
        title_slice = description.split()[start_choice : start_choice + 5]
        title = "{} {}".format(
            " ".join(title_slice).capitalize(), str(choice(range(100)))
        )
        target_date = date(2019, 5, 1)
        product_area = choice(PRODUCT_AREA_IDS)
        client_priority = CLIENT_PRIORITIES[client_id - 1].pop(choice(range(1, 10)))

        feature_request = FeatureRequest(
            title=title,
            description=description,
            target_date=target_date,
            client_id=client_id,
            client_priority=client_priority,
            product_area_id=product_area,
        )
        db_session.add(feature_request)

    db_session.commit()
