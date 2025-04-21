import torch

# Vérifie si CUDA est disponible
if torch.cuda.is_available():
    print("CUDA est disponible !")
    print(f"Nom du GPU : {torch.cuda.get_device_name(0)}")
    print(f"Nombre de GPU disponibles : {torch.cuda.device_count()}")
    print(f"GPU utilisé : {torch.cuda.current_device()}")
else:
    print("CUDA n'est PAS disponible. PyTorch utilise le CPU.")

# Création d'un tenseur sur le GPU
x = torch.rand(3, 3).to("cuda")
y = torch.rand(3, 3).to("cuda")
z = x + y
print(z)

