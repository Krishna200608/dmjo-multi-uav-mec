"""
Configuration - MAPPO Multi-UAV MEC Joint Optimization
======================================================
Final project direction: a plain MAPPO-based multi-UAV MEC approach with
trajectory control, task offloading, cooperative caching, NOMA scheduling,
jamming, and wind. Diffusion actor code is retained only as legacy optional
experiment code and is not part of the claimed method.
"""

import numpy as np

# ============================================================
# 1. AREA & DEPLOYMENT
# ============================================================
AREA_RADIUS   = 500
NUM_USERS     = 100
MAX_NUM_USERS = 180
NUM_UAVS      = 5
MAX_UAVS      = 8
MIN_UAVS      = 3
NUM_JAMMERS   = 1

# ============================================================
# 2. HETEROGENEOUS UAV PROFILES
# ============================================================
UAV_PROFILES = [
    {'cpu_freq': 3.0e9, 'cache_capacity': 150, 'cache_programs': 14,
     'bandwidth': 15e6, 'tx_power_dbm': 27, 'altitude': 110,
     'max_displacement': 55, 'max_concurrent': 20},
    {'cpu_freq': 2.0e9, 'cache_capacity': 100, 'cache_programs': 10,
     'bandwidth': 10e6, 'tx_power_dbm': 25, 'altitude': 100,
     'max_displacement': 50, 'max_concurrent': 15},
    {'cpu_freq': 1.2e9, 'cache_capacity': 60,  'cache_programs': 6,
     'bandwidth': 8e6,  'tx_power_dbm': 22, 'altitude': 85,
     'max_displacement': 60, 'max_concurrent': 10},
    {'cpu_freq': 2.5e9, 'cache_capacity': 120, 'cache_programs': 12,
     'bandwidth': 12e6, 'tx_power_dbm': 26, 'altitude': 105,
     'max_displacement': 52, 'max_concurrent': 18},
    {'cpu_freq': 1.8e9, 'cache_capacity': 80,  'cache_programs': 8,
     'bandwidth': 9e6,  'tx_power_dbm': 24, 'altitude': 95,
     'max_displacement': 58, 'max_concurrent': 12},
    {'cpu_freq': 2.8e9, 'cache_capacity': 130, 'cache_programs': 13,
     'bandwidth': 14e6, 'tx_power_dbm': 26, 'altitude': 108,
     'max_displacement': 53, 'max_concurrent': 19},
    {'cpu_freq': 1.5e9, 'cache_capacity': 70,  'cache_programs': 7,
     'bandwidth': 8.5e6,'tx_power_dbm': 23, 'altitude': 90,
     'max_displacement': 62, 'max_concurrent': 11},
    {'cpu_freq': 3.2e9, 'cache_capacity': 160, 'cache_programs': 15,
     'bandwidth': 16e6, 'tx_power_dbm': 28, 'altitude': 115,
     'max_displacement': 50, 'max_concurrent': 22},
]
NUM_UAV_CAPABILITY_DIMS = 5

# Rotary-wing propulsion model constants (Paper §III.E)
P1_BLADE           = 79.86
P2_INDUCED         = 88.63
ROTOR_TIP_SPEED    = 120
MEAN_ROTOR_VELOCITY = 4.03
DRAG_RATIO         = 0.6
AIR_DENSITY        = 1.225
ROTOR_SOLIDITY     = 0.05
DISC_AREA          = 0.503

# ============================================================
# 3. COMMUNICATION (Paper §III.C)
# ============================================================
RBS_BANDWIDTH         = 10e6
NUM_SUBCHANNELS       = 5
IOT_TX_POWER_DBM      = 20
JAMMER_TX_POWER_DBM   = 20
ENV_CONSTANT_A        = 9.6177
ENV_CONSTANT_B        = 0.1581
PATH_LOSS_EXPONENT    = 2.5
LOS_ATTENUATION_DB    = 0
NLOS_ATTENUATION_DB   = -20
NOISE_PSD_DBM         = -130
CARRIER_FREQUENCY     = 2e9
RICIAN_K_FACTOR       = 10
CHANNEL_POWER_GAIN_REF = 1e-4

# Jammer model
JAMMER_INTERFERENCE_RADIUS      = 120
JAMMER_PROXIMITY_PENALTY_RADIUS = 180
JAMMER_PROXIMITY_PENALTY_SCALE  = 2.0

# Variable per-device transmit power range
IOT_TX_POWER_MIN_DBM = 15
IOT_TX_POWER_MAX_DBM = 23

# Wind model — Ornstein-Uhlenbeck process
WIND_DRAG_COEFFICIENT      = 0.05
WIND_DIRECTION_CHANGE_RATE = 0.1
WIND_SPEED_MEAN            = 2.5
WIND_SPEED_REVERSION       = 0.08
WIND_SPEED_VOLATILITY      = 0.4
WIND_SPEED_MIN             = 0.0
WIND_SPEED_MAX             = 8.0
WIND_DRAG_QUADRATIC_COEFF  = 0.012   # W·s²/m²
WIND_K_DEGRADATION_FACTOR  = 0.06    # LoS degradation per m/s wind
IOT_WIND_DRIFT_FACTOR      = 0.12    # IoT displacement fraction of wind speed

# ============================================================
# 4. NOMA (Paper §III.D)
# ============================================================
PAIRING_WEIGHT_CHANNEL = 0.5
PAIRING_WEIGHT_FILE    = 0.5

# ============================================================
# 5. CACHING (Paper §III.D and §IV.C)
# ============================================================
ZIPF_EXPONENT        = 1.0
FILE_SIZE_MAX        = 100
FILE_SIZE_GAMMA      = 0.15
NUM_SERVICE_PROGRAMS = 20
PROGRAM_SIZES        = (1, 5)
MAB_EXPLORATION_COEFF = 1.0
MAB_POPULARITY_DECAY  = 0.3

# Two-timescale macro-interval length K_c (Paper §IV.A–IV.B).
# Both UAV trajectory updates and cache refreshes occur every K_c slots.
CACHE_UPDATE_INTERVAL = 25
MACRO_TIMESCALE_K_C   = CACHE_UPDATE_INTERVAL
A2A_BANDWIDTH         = 5e6
OFFLOAD_DELAY_COOPERATIVE = 0.05
OFFLOAD_DELAY_BS          = 0.40
OFFLOAD_ENERGY_PER_BIT    = 1e-7
CACHE_HIT_REWARD    = 1.0
CACHE_COOP_REWARD   = 0.5
CACHE_MISS_PENALTY  = -0.5

# ============================================================
# 6. TASK AND COMPUTATION MODEL (Paper §III.E)
# ============================================================
IOT_CPU_FREQUENCY     = 0.5e9
EFFECTIVE_CAPACITANCE = 1e-28

TASK_DATA_SIZE_RANGE  = (0.5e6, 5e6)
TASK_DATA_SIZE        = 2.75e6
TASK_CPU_CYCLES_RANGE = (0.1e9, 1e9)
TASK_DEADLINE_RANGE   = (0.2, 2.0)
TASK_GENERATION_PROB  = 0.7
NUM_TASK_TYPES        = 8
LOCAL_COMPUTE_THRESHOLD_FACTOR = 1.5

REWARD_LOCAL_COMPUTE = 0.5
REWARD_UAV_COMPUTE   = 1.5
REWARD_COMPUTE_FAIL  = -1.0

# ============================================================
# 7. ENERGY, LATENCY AND TIME
# ============================================================
IOT_ENERGY_BUFFER_MAX = 1.0
MIN_TRANSMISSION_BITS = 1e5

TOTAL_TIME     = 500
NUM_TIME_SLOTS = 500
SLOT_DURATION  = TOTAL_TIME / NUM_TIME_SLOTS
TIME_DIVISION_FACTOR = 0.5

# IoT Gauss-Markov mobility (Paper §III.B, Eqs. 1–4)
GM_RHO_V     = 0.9    # speed memory ρ_v
GM_RHO_THETA = 0.75   # heading memory ρ_θ
GM_MEAN_SPEED = 1.0   # mean speed v̄ (m/slot)
GM_SIGMA_V    = 0.4   # speed noise std σ_v
GM_SIGMA_THETA = 0.4  # heading noise std σ_θ

VIDEO_RENDER_SUBSTEPS = 4
VIDEO_PLOT_STEPS      = 200

# Set False to skip periodic mid-training videos (overridable via --no-training-video)
ENABLE_TRAINING_VIDEO = False

# ============================================================
# 8. LEGACY ACTOR EXPERIMENT SETTINGS
# ============================================================
# These constants are kept so old checkpoints/scripts that import the
# diffusion actor module do not break. The final project does not enable
# diffusion in any default or documented run.
DIFFUSION_DENOISING_STEPS = 3
DIFFUSION_BETA_A          = 0.1
DIFFUSION_BETA_B          = 20.0
DIFFUSION_HIDDEN_DIM      = 256

# ============================================================
# 9. MAPPO TRAINING
# ============================================================
MAPPO_LR_ACTOR        = 3e-4
MAPPO_LR_CRITIC       = 1e-4
MAPPO_GAMMA           = 0.99
MAPPO_GAE_LAMBDA      = 0.95
MAPPO_CLIP_EPS        = 0.2
MAPPO_ENTROPY_COEF    = 0.01
MAPPO_VALUE_COEF      = 0.5
MAPPO_MAX_GRAD_NORM   = 0.5
MAPPO_ROLLOUT_LENGTH  = 500
MAPPO_NUM_MINI_BATCHES = 5
MAPPO_PPO_EPOCHS      = 4
MAPPO_HIDDEN_DIM      = 256
MAPPO_CRITIC_HIDDEN_DIM = 512

TOTAL_TIMESTEPS       = 5_000_000
EVAL_INTERVAL         = 50_000
VIDEO_INTERVAL        = 100_000
VIDEO_STOP_AFTER      = 0
CHECKPOINT_INTERVAL   = 500_000
LOG_INTERVAL          = 20_000
SERVICE_PERIOD_SLOTS  = NUM_TIME_SLOTS

# ============================================================
# 10. DOMAIN RANDOMISATION
# ============================================================
DOMAIN_RAND_INTERVAL             = 100_000
RAND_NUM_USERS                   = (80, 150)
RAND_NUM_UAVS                    = (3, 8)
RAND_NUM_JAMMERS                 = (1, 3)
RAND_JAMMER_POWER_DBM            = (15, 25)
RAND_AREA_RADIUS                 = (400, 600)
RAND_IOT_TX_POWER_DBM            = (15, 23)
RAND_NOISE_PSD_DBM               = (-135, -125)
RAND_WIND_SPEED                  = (0.0, 5.0)
RAND_JAMMER_INTERFERENCE_RADIUS  = (80, 160)

# ============================================================
# 11. OBJECTIVE WEIGHTS
# ============================================================
ALPHA_LATENCY = 0.6
BETA_ENERGY   = 0.4

# ============================================================
# 12. ABLATION FLAGS
# ============================================================
# Supported modes (set via --ablation CLI flag in train.py):
#   "full"             - complete MAPPO MEC framework (default)
#   "single_timescale" - K_c = 1, every slot is a macro step
#   "no_diffusion"     - legacy alias; same actor as full because final MAPPO
#                        is already non-diffusion
#   "no_mappo_traj"    - fixed circular UAV orbits
#   "no_coop_cache"    - local + BS only, tier-2 A2A disabled
#   "minimal"          - no cooperative cache, plain MAPPO actor
ABLATION_MODE    = "full"

USE_DIFFUSION    = False   # Final project uses Gaussian MAPPO, not diffusion.
USE_COOP_CACHE   = True    # False -> skip tier-2 A2A fetch.
USE_LEARNED_TRAJ = True    # False -> fixed circular orbit.
CACHE_TIMESCALE_K_C = MACRO_TIMESCALE_K_C   # set to 1 for single_timescale

ABLATION_CHOICES = (
    "full",
    "single_timescale",
    "no_diffusion",
    "no_mappo_traj",
    "no_coop_cache",
    "minimal",
)


def resolve_ablation(mode: str = "full") -> dict:
    """Return the runtime ablation settings for a named MAPPO-MEC variant."""
    if mode not in ABLATION_CHOICES:
        raise ValueError(f"Unknown ablation mode {mode!r}. Choose from {ABLATION_CHOICES}.")

    settings = {
        "full": {
            "mode": "full",
            "use_diffusion": False,
            "use_coop_cache": True,
            "use_learned_traj": True,
            "cache_timescale_k_c": CACHE_UPDATE_INTERVAL,
        },
        "single_timescale": {
            "mode": "single_timescale",
            "use_diffusion": False,
            "use_coop_cache": True,
            "use_learned_traj": True,
            "cache_timescale_k_c": 1,
        },
        "no_diffusion": {
            "mode": "no_diffusion",
            "use_diffusion": False,
            "use_coop_cache": True,
            "use_learned_traj": True,
            "cache_timescale_k_c": CACHE_UPDATE_INTERVAL,
        },
        "no_mappo_traj": {
            "mode": "no_mappo_traj",
            "use_diffusion": False,
            "use_coop_cache": True,
            "use_learned_traj": False,
            "cache_timescale_k_c": CACHE_UPDATE_INTERVAL,
        },
        "no_coop_cache": {
            "mode": "no_coop_cache",
            "use_diffusion": False,
            "use_coop_cache": False,
            "use_learned_traj": True,
            "cache_timescale_k_c": CACHE_UPDATE_INTERVAL,
        },
        "minimal": {
            "mode": "minimal",
            "use_diffusion": False,
            "use_coop_cache": False,
            "use_learned_traj": True,
            "cache_timescale_k_c": CACHE_UPDATE_INTERVAL,
        },
    }
    return dict(settings[mode])


def apply_ablation(mode: str = "full") -> dict:
    """Apply a named ablation to module-level config and return its settings."""
    global ABLATION_MODE, USE_DIFFUSION, USE_COOP_CACHE
    global USE_LEARNED_TRAJ, CACHE_TIMESCALE_K_C

    settings = resolve_ablation(mode)
    ABLATION_MODE = settings["mode"]
    USE_DIFFUSION = settings["use_diffusion"]
    USE_COOP_CACHE = settings["use_coop_cache"]
    USE_LEARNED_TRAJ = settings["use_learned_traj"]
    CACHE_TIMESCALE_K_C = settings["cache_timescale_k_c"]
    return settings


def current_ablation_config() -> dict:
    """Return the currently active runtime ablation settings."""
    return {
        "mode": ABLATION_MODE,
        "use_diffusion": USE_DIFFUSION,
        "use_coop_cache": USE_COOP_CACHE,
        "use_learned_traj": USE_LEARNED_TRAJ,
        "cache_timescale_k_c": CACHE_TIMESCALE_K_C,
    }

# ============================================================
# DERIVED CONSTANTS
# ============================================================
def dbm_to_watt(dbm):
    return 10 ** ((dbm - 30) / 10)

def db_to_linear(db):
    return 10 ** (db / 10)

IOT_TX_POWER     = dbm_to_watt(IOT_TX_POWER_DBM)
JAMMER_TX_POWER  = dbm_to_watt(JAMMER_TX_POWER_DBM)
NOISE_PSD        = dbm_to_watt(NOISE_PSD_DBM)
LOS_ATTENUATION  = db_to_linear(LOS_ATTENUATION_DB)
NLOS_ATTENUATION = db_to_linear(NLOS_ATTENUATION_DB)
IOT_TX_POWER_MIN = dbm_to_watt(IOT_TX_POWER_MIN_DBM)
IOT_TX_POWER_MAX = dbm_to_watt(IOT_TX_POWER_MAX_DBM)

UAV_ALT_MIN       = 50.0
UAV_ALT_MAX       = 150.0
UAV_ALT_DELTA_MAX = 10.0
