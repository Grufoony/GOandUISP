"""
Script to generate a synthetic dataset for testing purposes. The dataset will
contain data about athletes participating in swimming competitions.
"""

import argparse
import random
import uuid
import pandas as pd
from faker import Faker
from tqdm import trange
from pathlib import Path
from goanduisp.core import STYLES, get_category

POSSIBLE_STYLES = list(STYLES.keys())
POSSIBLE_DISTANCES = [50, 100, 200]

# Initialize Faker and random seed for reproducibility
fake = Faker()


# Define helper functions for synthetic data generation
def gen_race_time():
    """Generates a synthetic race time in the format MM'SS"SS"""
    minutes = random.randint(20, 60)
    seconds = random.randint(0, 59)
    milliseconds = random.randint(0, 99)
    return f"{minutes:02d}'{seconds:02d}\"{milliseconds:02d}"


def gen_final_position():
    """Generates a random final position for an athlete in the race"""
    return random.randint(1, 20)


def gen_lane_number():
    """Generates a random lane number between 1 and 8"""
    return random.randint(1, 8)


def gen_athlete(club, n_races, pool_size):
    # disable pylint too many local variables
    # pylint: disable=R0914
    """Generates multiple rows for a single athlete"""
    club_name = club
    athlete_id = str(uuid.uuid4()).replace("-", "")
    full_name = fake.name().upper()
    sex = random.choice(["M", "F"])
    birth_year = random.randint(1980, 2015)
    relay_team_id = None
    relay_team_name = None
    category_id = get_category(sex=sex, year=birth_year)
    name, surname = full_name.split()[:2]
    fiscal_code = fake.ssn()
    athlete_category_id = random.randint(1, 5)
    relay_team_subtitle = None
    relay_team_member_count = None

    athlete_rows = []

    for _ in range(n_races):
        event_race_member_id = str(uuid.uuid4()).replace("-", "")
        race_id = str(uuid.uuid4()).replace("-", "")
        style_id = random.choice(POSSIBLE_STYLES)
        length = random.choice(POSSIBLE_DISTANCES)
        description = f"{length} {STYLES[style_id].upper()} {category_id} {sex}"
        internal_group_nr = None
        lane_nr = gen_lane_number()
        official_time = gen_race_time()
        race_time = gen_race_time()
        final_position = gen_final_position()
        point = random.randint(0, 100)
        point2 = f"{random.uniform(0, 100):.2f}".replace(".", ",")
        calculation_flag = random.choices(["A", None], [0.3, 0.7])[0]
        race_status = None if calculation_flag == "A" else "T"

        athlete_rows.append(
            [
                event_race_member_id,
                club_name,
                athlete_id,
                full_name,
                sex,
                birth_year,
                relay_team_id,
                relay_team_name,
                category_id,
                description,
                style_id,
                length,
                pool_size,
                race_id,
                "D",  # RaceLevel
                internal_group_nr,
                lane_nr,
                official_time,
                race_time,
                final_position,
                calculation_flag,
                race_status,
                point,
                point2,
                relay_team_subtitle,
                relay_team_member_count,
                athlete_category_id,
                name,
                surname,
                fiscal_code,
            ]
        )

    return athlete_rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synthetic dataset generator")
    parser.add_argument(
        "-s", "--seed", type=int, default=69, help="Seed for random number generator."
    )
    parser.add_argument(
        "--pool-size", type=int, default=25, help="Pool size in meters (25 or 50)"
    )
    parser.add_argument(
        "-na",
        "--n-athletes",
        type=int,
        default=30,
        help="Number of athletes to generate",
    )
    parser.add_argument(
        "-mnr",
        "--max-n-races",
        type=int,
        default=4,
        help="Max number of races per athlete",
    )
    args = parser.parse_args()
    Faker.seed(args.seed)
    random.seed(args.seed)
    POSSIBLE_CLUBS = [fake.company() for _ in range(args.n_athletes // 10)]
    data = []

    # Generate synthetic data
    for _ in trange(args.n_athletes):
        athletes_rows = gen_athlete(
            random.choice(POSSIBLE_CLUBS),
            random.randint(1, args.max_n_races),
            args.pool_size,
        )
        data.extend(athletes_rows)

    # Create a DataFrame from the data
    COLUMNS = [
        "EventRaceMemberId",
        "ClubName",
        "AthleteId",
        "Fullname",
        "Sex",
        "BirthYear",
        "RelayTeamId",
        "RelayTeamName",
        "CategoryId",
        "Description",
        "StyleId",
        "Length",
        "PoolSize",
        "RaceId",
        "RaceLevel",
        "InternalGroupNr",
        "LaneNr",
        "OfficialTime",
        "RaceTime",
        "FinalPosition",
        "CalculationFlag",
        "RaceStatus",
        "Point",
        "Point2",
        "RelayTeamSubtitle",
        "RelayTeamMemberCount",
        "AthleteCategoryId",
        "Name",
        "Surname",
        "FiscalCode",
    ]

    df = pd.DataFrame(data, columns=COLUMNS)

    # Save to CSV (semicolon separated)
    script_dir = Path(__file__).parent
    output_path = script_dir / "synthetic_race_data.csv"
    df.to_csv(output_path, sep=";", index=False)

    print(f"Synthetic dataset generated and saved as '{output_path}'.")
