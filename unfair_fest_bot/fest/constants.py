"""
    Some constants may be unused, but could be useful for things you might add to the bot.
"""

BASE_FEST_API_URL = "https://private-tournaments-api.bikerace.com/"

ONE_STAR_BIKES = ["1_A", "1_C", "1_E", "1_G", "1_H", "1_I", "1_R", "1_S", "1_T"]

TWO_STAR_BIKES = ["2_A", "2_C", "2_E", "2_G", "2_H", "2_I", "2_R", "2_S", "2_T"]

THREE_STAR_BIKES = [
    "3_A_H",
    "3_A_S",
    "3_C_A",
    "3_H_E",
    "3_H_T",
    "3_I",
    "3_R_C",
    "3_R_G",
    "3_T_S",
]

FOUR_STAR_BIKES = [
    "4_C_A_H",
    "4_H_T_E",
    "4_H_T_S",
    "4_I",
    "4_R_A_G",
    "4_R_C_A",
    "4_R_G_S",
]

FIVE_STAR_BIKES = ["5_H_T_E_S", "5_R_A_G_S", "5_R_C_A_H"]

TOURNEY_REQUIREMENTS_TYPES = ["descriptor", "powers", "min_category"]

# BikePowerNames with it's character that means the power.
TOURNEY_REQUIREMENT_POWERS = {
    "BikePowerAcrobatic": "A",
    "BikePowerReverse": "R",
    "BikePowerAllWheel": "T",
    "BikePowerUnbreakable": "C",
    "BikePowerHog": "H",
    "BikePowerGhost": "G",
    "BikePowerTurbo": "S",
    "BikePowerExtraChance": "E",
}
