from otree.common import safe_json
import json




def chart_for_admin(me):
    if final:
        all_contribs = [[r.round_number, (a.contribution or 0)] for r in mysubsession.in_all_rounds() for a in
                        r.get_players()]
        all_contribs += making_add
        popsize = len(mysubsession.get_players())
        all_contribs_average = [[r.round_number, round(sum([(p.contribution or 0) for p in r.get_players()]) / popsize)]
                                for r in mysubsession.in_all_rounds()]

        series.append({
            'name': 'All participants',
            'type': 'scatter',
            'data': all_contribs,
            'marker': {
                'fillColor': '#FFFFFF',
                'lineWidth': 1,
                'lineColor': 'blue',
                'symbol': 'circle',
                'radius': 7,
            }})
        series.append({
            'name': 'Overall average',
            'type': 'line',
            'color': 'rgba(0, 0, 0, 0.2)',
            'lineWidth': 15,
            'data': all_contribs_average,
            'marker': {
                'enabled': False,
                'fillColor': '#FFFFFF',
                'lineWidth': 1,
                'lineColor': 'blue',
                'radius': 1,
                'symbol': 'circle',
            }})
