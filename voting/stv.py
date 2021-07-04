import pandas as pd

LOG_FILE = './log.txt'


def rank_stv(df, log=True):
    """
    Calculate the result a single transferrable vote.

    Choices are eliminated in rounds. The choice with the fewest first-preference votes is eliminated in each round.

    If a voter had chosen the eliminated candidate as their first choice, their ranking of the remaining candidates is
    used to redistribute their single vote.

    Ties are resolved using a recursive runoff to determine the choice with the least consent.

    Candidates are removed in each round until a single candidate with a majority of first preference votes remains.
    """
    if log == True:
        log_file = open(LOG_FILE, 'w')

        def log_output(output):
            print(output, file=log_file)
    else:
        def log_output(output):
            print(output)

    round_losers = {}
    max_rounds = len(df)
    round_no = 0
    winner = None

    while round_no < max_rounds:
        round_no += 1
        first_preference_votes = count_nth_preference_votes(df, n=1)
        has_majority = is_winner(first_preference_votes, df)
        winner_exists = has_majority.any()
        if winner_exists:
            winner = has_majority.loc[has_majority == True].index[0]
            log_output('The winner is {} in round {}'.format(winner, round_no))

        log_output(f'Round {round_no} table:')
        log_output(df)
        log_output('\n')

        round_loser = determine_losing_choice(df, first_preference_votes, log_output)
        if round_no < max_rounds:
            log_output('Round {} loser: {}'.format(round_no, round_loser))

        round_losers.update({round_no: round_loser})

        df = transfer_vote_for_voters_who_have_loser_ranked_first(df, round_loser)
        df = remove_choice(df, round_loser)
        log_output('\n')

    log_output(f'The winner is: {winner}')
    if log == True:
        log_file.close()

    final_ranking = pd.Series(round_losers, name='Accommodation')
    final_ranking.index.name = 'Ranking'
    # Candidates are ranked in the reverse order of the round numbers they were limited on
    final_ranking.index = final_ranking.index.max() - (final_ranking.index - 1)
    return pd.DataFrame(final_ranking.sort_index(ascending=True))


def count_nth_preference_votes(df, n=1):
    return df[df == n].sum(axis='columns')


def is_winner(votes, df):
    number_of_voters = len(df.columns)
    has_majority = votes > number_of_voters * 0.5
    return has_majority


def determine_losing_choice(df, votes, output_log, recursion_level=0):
    """
    Determine the choice with the fewest first-preference votes. If there is a tie, decrement rankings amongst the tied
    choices and determine the loser using a recursive runoff vote.
    """
    lowest_votes = votes.min()
    losing_choices = votes.loc[votes == lowest_votes]

    if len(losing_choices) == 1:
        return losing_choices.index[0]
    else:
        indent = (recursion_level + 1) * '\t'
        output_log(indent + 'tied losers: {}\n'.format([x for x in losing_choices.index]))

        losing_votes = df.loc[losing_choices.index]

        for voter in losing_votes.columns:
            losing_votes[voter] -= 1
            losing_votes.loc[losing_votes[voter] < 1, voter] = 1

        votes_for_losers = count_nth_preference_votes(losing_votes, n=1)
        return determine_losing_choice(losing_votes, votes_for_losers, output_log, recursion_level=recursion_level + 1)


def transfer_vote_for_voters_who_have_loser_ranked_first(df, loser):
    rank_given_to_loser = df.loc[loser]
    voters_who_preferred_loser = rank_given_to_loser.loc[rank_given_to_loser == 1].index

    for voter in voters_who_preferred_loser:
        voters_choices = df[voter].sort_values()

        rank = 1
        for choice, rank_given in voters_choices.iteritems():
            if choice != loser:
                df.loc[choice, voter] = rank
                rank += 1
    return df


def remove_choice(df, loser):
    return df.drop(loser)
