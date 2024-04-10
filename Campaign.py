import enum


class CampaignState(enum.Enum):
    NONE = -1,
    CREATED = 0,
    BUILDING_CHARACTER = 1


class Campaign:
    # Campaign state for delete command
    campaign_state = CampaignState.NONE

    player_confirm_delete = []

    # Server ID
    CAMPAIGN_GUILD_ID: int = 0

    # General attributes
    players_num: int = 0
    ready_players_num: int = 0

    PLAYER_NUM_MSG_ID: int = 0

    campaign_member_list = []

    has_dm_already: bool = False

    players_selected_race = []
    players_selected_class = []

    def __init__(self, user_num: int, guild_id: int):
        self.players_num = user_num
        self.CAMPAIGN_GUILD_ID = guild_id
        self.has_dm_already = False
        self.campaign_state = CampaignState.CREATED

    def check_if_can_start_campaign(self):
        if self.players_num == self.ready_players_num and self.has_dm_already:
            return True
        return False

    def add_ready_player(self):
        self.ready_players_num += 1

    def remove_ready_player(self):
        self.ready_players_num -= 1

    def get_member(self, member_name: str):
        for member in self.campaign_member_list:
            if member.member.name == member_name:
                return member
        return None
        