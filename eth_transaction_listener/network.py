import torch
import os


class Network:

    def __init__(self):
        self.network = self.load_network()
        self.mean = torch.load(self.get_model_path('mlp-mean.pt'), map_location="cpu")
        self.std = torch.load(self.get_model_path('mlp-std.pt'), map_location="cpu")

    def get_model_path(self, model_name):
        cwd = os.getcwd()
        keyword = 'frontrunning-attacks'
        parts = cwd.split(keyword)
        root_path = os.path.join(parts[0], keyword)
#        root_path = os.path.dirname(os.getcwd())
        model_data_path = os.path.join(root_path, 'model', model_name)

        return model_data_path

    def load_network(self):
        network = MLP()
        network.load_state_dict(torch.load(self.get_model_path('front-running-attack-model.pth'), map_location="cpu"))
        return network.eval()

    def get_prediction(self, x):
        x_tensor = torch.tensor(x)
        x_standardized = (x_tensor - self.mean) / self.std
        with torch.no_grad():
            tensor = x_standardized.clone().detach().view(1, 7)
            prediction = self.network(tensor.clone().detach().to(torch.float32)).item()
            return prediction > 0.5


class MLP(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = torch.nn.Sequential(
            torch.nn.Linear(7, 10),  # Input layer to first hidden layer
            torch.nn.Sigmoid(),  # Sigmoid activation function for the first hidden layer
            torch.nn.Linear(10, 10),  # First hidden layer to second hidden layer
            torch.nn.Sigmoid(),  # Sigmoid activation function for the second hidden layer
            torch.nn.Linear(10, 1)
        )

    def forward(self, x):
        return self.layers(x)
