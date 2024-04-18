import yaml


class ContainerModelLogicTemplate:

    def cos_sim_of_words(self, w1, w2):
        """
        template function for calculating cosine similarity between two words

        Parameters:
        w1 (str): One of two words
        w2 (str): One of two words

        Returns:
        float: cosine similarity, ranging from 0 to 1 
        """

        pass


def calculate_closeness_score(word_base, word_close, word_distant, cos_sim_func):

    # calculate cosine similarities with given function
    sim_base_close = cos_sim_func(word_base, word_close)
    sim_base_distant = cos_sim_func(word_base, word_distant)
    print(f"cosine simliarity between '{word_base}' and '{word_close}': {sim_base_close}")
    print(f"cosine simliarity between '{word_base}' and '{word_distant}': {sim_base_distant}")

    # calculate score
    score = (sim_base_close - sim_base_distant - (1 - sim_base_close) + 0.5) * 2 / 3
    print(f"score: {score}")

    return score


def calculate_synonym_score(synonym_data_list, cos_sim_fun):
    score_list = []

    # iterate over synonyms
    for synonym_data in synonym_data_list:

        # extract words
        word_base = synonym_data[0]
        word_synonym = synonym_data[1]
        word_random = synonym_data[2]

        # call function and append result
        score = calculate_closeness_score(
            word_base=word_base,
            word_close=word_synonym,
            word_distant=word_random,
            cos_sim_func=cos_sim_fun,
        )
        score_list.append(score)

    # calculate average of all scores
    score_avg = round(sum(score_list) / len(score_list), 2)
    print("------------------------------------------------")
    print(f"total average synonym score: {score_avg}")


def calculate_homonym_score(homonym_data_list, cos_sim_fun):
    score_list = []

    # iterate over homonyms
    for homonym_data in homonym_data_list:

        # extract words
        word_base = homonym_data[0]
        word_related_1 = homonym_data[1]
        word_related_2 = homonym_data[2]
        word_random = homonym_data[3]

        # call function with both related homonym neighbor words, average result, append
        score_1 = calculate_closeness_score(
            word_base=word_base,
            word_close=word_related_1,
            word_distant=word_random,
            cos_sim_func=cos_sim_fun,
        )
        score_2 = calculate_closeness_score(
            word_base=word_base,
            word_close=word_related_2,
            word_distant=word_random,
            cos_sim_func=cos_sim_fun,
        )
        score = (score_1 + score_2) / 2
        print(f"average score: {score}")
        score_list.append(score)

    score_avg = round(sum(score_list) / len(score_list), 2)
    print("------------------------------------------------")
    print(f"total average homonym score: {score_avg}")


def calculate_antonym_score(antonym_data_list, cos_sim_fun):
    score_list = []

    # iterate over antonyms
    for antonym_data in antonym_data_list:
        word_base = antonym_data[0]
        word_antonym = antonym_data[1]
        word_synonym = antonym_data[2]

        # call function and append result
        score = calculate_closeness_score(
            word_base=word_base,
            word_close=word_synonym,
            word_distant=word_antonym,
            cos_sim_func=cos_sim_fun,
        )
        score_list.append(score)

    # calculate average of all scores
    score_avg = round(sum(score_list) / len(score_list), 2)
    print("------------------------------------------------")
    print(f"total average antonym score: {score_avg}")


def calculate_eval_score(eval_data_file, container_model_logic):

    with open(eval_data_file) as f:
        eval_data = yaml.safe_load(f)

        print("\ncalculating synonyms score")
        calculate_synonym_score(eval_data["synonyms"], container_model_logic.cos_sim_of_words)
        
        print("\ncalculating homonyms score")
        calculate_homonym_score(eval_data["homonyms"], container_model_logic.cos_sim_of_words)
        
        print("\ncalculating antonyms score")
        calculate_antonym_score(eval_data["antonyms"], container_model_logic.cos_sim_of_words)

