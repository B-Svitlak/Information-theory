from decimal import Decimal, getcontext
from collections import Counter, OrderedDict


class ArithmeticEncoding:
    """
    ArithmeticEncoding is a class for building arithmetic encoding.
    """

    def __init__(self, frequency_table):
        self.probability_table = self.get_probability_table(frequency_table)

    @staticmethod
    def get_probability_table(text):
        """
        Calculates the probability table out of the frequency table.
        """
        probs = dict(sorted(Counter(text).items(), key=lambda value: value[1], reverse=True))
        total_frequency = sum(probs.values())

        probability_table = OrderedDict()
        for key, value in probs.items():
            probability_table[key] = value / Decimal(total_frequency)
        return probability_table

    @staticmethod
    def process_stage(probability_table, stage_min, stage_max):
        """
        Processing a stage in the encoding.
        """
        stage_probs = {}
        stage_domain = stage_max - stage_min
        for term, term_prob in probability_table.items():
            cum_prob = term_prob * stage_domain + stage_min
            stage_probs[term] = [stage_min, cum_prob]
            stage_min = cum_prob
        return stage_probs

    def encode(self, msg):
        """
        Encodes a message.
        """
        stage_min, stage_max = Decimal(0.0), Decimal(1.0)

        for msg_term in msg:
            stage_probs = self.process_stage(self.probability_table, stage_min, stage_max)
            stage_min, stage_max = stage_probs[msg_term]

        test1 = (stage_max - stage_min) / 2
        return test1 + stage_min

    def decode(self, encoded_msg, length):
        """
        Decodes a message.
        """
        decoded_msg = ""

        stage_min, stage_max = Decimal(0.0), Decimal(1.0)
        stage_probs = self.process_stage(self.probability_table, stage_min, stage_max)

        for idx in range(length):
            for msg_term, value in stage_probs.items():
                if value[0] <= encoded_msg <= value[1]:
                    break
            decoded_msg += msg_term
            stage_min, stage_max = stage_probs[msg_term]
            encoded_msg = (encoded_msg - stage_min) / (stage_max - stage_min)

        return decoded_msg


if __name__ == '__main__':
    getcontext().prec = 45
    text = 'Хіба ревуть воли, як ясла повні?'

    A = ArithmeticEncoding(text)
    encoded_msg = A.encode(text)
    print(encoded_msg)

    decoded_msg = A.decode(Decimal(encoded_msg), len(text))
    print("Decoded Message: {msg}".format(msg=decoded_msg))
