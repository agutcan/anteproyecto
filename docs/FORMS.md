# Formularios Clave

## 1. Registro
- Valida email único
- Password con complexity rules

## 2. Crear Torneo (VIP)
```python
class TournamentForm(forms.ModelForm):
    def clean_max_teams(self):
        # Valida 2/4/8 equipos (como mencionas)
        if max_teams not in [2, 4, 8]:
            raise ValidationError("Solo 2, 4 u 8 equipos")
```
