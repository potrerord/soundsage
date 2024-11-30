ACOUSTICNESS_MIN: float = 0.0
ACOUSTICNESS_MAX: float = 1.0

DANCEABILITY_MIN: float = 0.0
DANCEABILITY_MAX: float = 1.0

ENERGY_MIN: float = 0.0
ENERGY_MAX: float = 1.0

INSTRUMENTALNESS_MIN: float = 0.0
INSTRUMENTALNESS_MAX: float = 1.0

KEY_NONE_DETECTED: int = -1
KEY_MIN: int = 0
KEY_MAX: int = 11

LIVENESS_MIN: float = 0.0
LIVENESS_MAX: float = 1.0

LOUDNESS_MIN_USEFUL: float = -60.0 # Not a pure limit, but a likely limit
LOUDNESS_MAX: float = 0.0

MODE_MINOR: int = 0
MODE_MAJOR: int = 1

SPEECHINESS_MIN: float = 0.0
SPEECHINESS_MAX: float = 1.0

TEMPO_MIN_USEFUL: float = 30.0 # Likely limit
TEMPO_MAX_USEFUL: float = 300.0 # Likely limit

TIME_SIG_MIN: int = 3
TIME_SIG_MAX: int = 7

VALENCE_MIN: float = 0.0
VALENCE_MAX: float = 1.0