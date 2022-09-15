import sys
sys.path.insert(0, '../')
import sleeper_wrapper as sw

league = '867609901030088704'

players = sw.Players()

players.get_all_players()