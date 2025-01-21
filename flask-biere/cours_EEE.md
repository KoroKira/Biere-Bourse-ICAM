# Électronique - Guide de référence

## 1. Formules fondamentales et lois
| Grandeur | Formule | Notes |
|----------|---------|-------|
| Fréquence | f = 1/T | T : période |
| Pulsation | ω = 2πf | rad/s |
| Loi d'Ohm | U = R × I | - |
| Puissance | P = U × I = R × I² = U²/R | - |
| Conductance | G = 1/R | Siemens [S] |

### Composants passifs
| Composant | Impédance | Relation U/I | Déphasage |
|-----------|-----------|--------------|------------|
| Résistance | R | U = R × I | 0 |
| Bobine | jLω | u(t) = L × di/dt | +π/2 |
| Condensateur | 1/jCω | i(t) = C × du/dt | -π/2 |

### Lois fondamentales et théorèmes
- **Nœuds** : ΣI entrants = ΣI sortants
- **Mailles** : ΣU tensions = 0
- **Millman** : U = (ΣUi/Ri)/(Σ1/Ri)
- **Générateurs** :
  - Tension : U = E - rI
  - Courant : I = Icc - U/R

### Thévenin et Norton
| Théorème | Modèle | Paramètres | Calculs |
|----------|---------|------------|---------|
| Thévenin | Source de tension + Rth | Eth, Rth | Eth = Vco, Rth = Eth/Icc |
| Norton | Source de courant + Rn | In, Rn | In = Icc, Rn = Vco/Icc |

#### Relations
| Conversion | Formules |
|------------|----------|
| Thévenin → Norton | In = Eth/Rth, Rn = Rth |
| Norton → Thévenin | Eth = In×Rn, Rth = Rn |

## 2. Régime sinusoïdal
## Triphasé
### Configurations principales

| Configuration | Tension Ligne (\(U\)) | Tension Phase (\(U_P\)) | Courant Ligne (\(I\)) | Courant Phase (\(I_P\)) | Puissance |
|---------------|------------------------|-------------------------|------------------------|--------------------------|-----------|
| **Étoile (Y)** | \(U = \sqrt{3} \, U_P\) | \(U_P = U / \sqrt{3}\) | \(I = I_P\) | \(I_P = I\) | \(P = \sqrt{3} \, U \, I \, \cos(\varphi)\) |
| **Triangle (Δ)** | \(U = U_P\) | - | \(I = \sqrt{3} \, I_P\) | \(I_P = I / \sqrt{3}\) | \(P = \sqrt{3} \, U \, I \, \cos(\varphi)\) |

### Notes importantes
1. **Étoile (Y)** :
   - Chaque phase est connectée entre une borne et le neutre.
   - Convient lorsque des tensions phase-neutre sont nécessaires.
2. **Triangle (Δ)** :
   - Chaque phase est connectée entre deux bornes.
   - Pas de neutre, donc uniquement des tensions ligne-ligne.

### Puissances dans un système triphasé

| Type de puissance | Formule | Unité |
|--------------------|---------|-------|
| Tension | u(t) = U√2 sin(ωt + φ) | V |
| Courant | i(t) = I√2 sin(ωt + φ) | A |
| Puissance active (\(P\)) | \(P = \sqrt{3} \, U \, I \, \cos(\varphi)\) | Watts (W) |
| Puissance réactive (\(Q\)) | \(Q = \sqrt{3} \, U \, I \, \sin(\varphi)\) | Volt-ampères réactifs (VAR) |
| Puissance apparente (\(S\)) | \(S = \sqrt{3} \, U \, I\) | Volt-ampères (VA) |
| Facteur de puissance (\(\text{fp}\)) | \(\text{fp} = \cos(\varphi)\) | - |

### Représentation vectorielle
- **Diagramme de Fresnel** : Les tensions des phases sont décalées de 120° entre elles.
- **Courants** : Alignés ou déphasés selon les impédances des charges.


## 3. ALI (Amplificateurs Linéaires Intégrés)
### Caractéristiques et règles
- Ad → ∞, Ze → ∞, Zs = 0
- V+ = V-, I+ = I- = 0 (régime linéaire)
- TRMC = 20log(Ad/Ac)

### Montages de base
| Type | Gain | Formule |
|------|------|---------|
| Suiveur | 1 | Vs = Ve |
| Inverseur | -R2/R1 | Vs = -(R2/R1)Ve |
| Non-inverseur | 1 + R2/R1 | Vs = (1 + R2/R1)Ve |
| Intégrateur | - | Vs = -(1/RC)∫Ve dt |
| Dérivateur | - | Vs = -RC(dVe/dt) |
| Comparateur | - | Vs = ±Vsat selon V+/V- |
| Comparateur à 2 seuils | - | Vs = ±Vsat selon V+/V-, attention au sens d'où l'on vient|

## 4. Convertisseurs et composants
### CAN/CNA
| Caractéristique | CAN | CNA |
|-----------------|-----|-----|
| Résolution | n bits | n bits |
| Quantum | q = VPE/2ⁿ | - |
| Erreur | ±q/2 | - |
| Types | SAR, Flash, Σ-Δ | R-2R, pondéré |

### Semi-conducteurs - Transistors
| Type | Caractéristiques | Polarisation | Applications |
|------|-----------------|--------------|--------------|
| NPN | β = Ic/Ib ≈ 100-300 | VBE ≈ 0.7V, VCE > VCE sat | Amplification courant |
| PNP | β = -Ic/Ib ≈ 100-300 | VEB ≈ 0.7V, VEC > VEC sat | Amplification courant |

#### Zones de fonctionnement
| Zone | Condition | Utilisation |
|------|-----------|-------------|
| Bloqué | VBE < 0.7V | Interrupteur ouvert |
| Saturation | VBE > 0.7V, VCE ≈ 0.2V | Interrupteur fermé |
| Actif linéaire | VBE ≈ 0.7V, VCE > VCE sat | Amplification |

#### Formules transistors
| Paramètre | NPN | PNP |
|-----------|-----|-----|
| Courant collecteur | Ic = β×Ib | Ic = -β×Ib |
| Courant émetteur | Ie = Ic + Ib | Ie = -(Ic + Ib) |
| Tension collecteur-émetteur | VCE > 0.2V (sat) | VEC > 0.2V (sat) |
| Gain en courant | hFE = Ic/Ib | hFE = -Ic/Ib |

### Autres semi-conducteurs
| Composant | Caractéristiques | Applications |
|-----------|------------------|--------------|
| Diode | Vseuil, Imax | Redressement, LED |
| Thyristor | Amorçage par gâchette | Puissance |
