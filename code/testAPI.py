def More(self):
    return f"Жанр: {self.find['genres'][0]['name']} \nРежиссер (или руководитель): {self.find['persons'][0]['name']} \n" \
           f"Премьера: {self.find['premiere']['world'][:4]} год."