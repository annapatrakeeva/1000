import random

import openmc
from openmc.data import NATURAL_ABUNDANCE
import math
from math import pi
import neutronics_material_maker as nmm

# обогащение 3.7
UO2_mat = openmc.Material(material_id=1, name='UO2', temperature=1027)
UO2_mat.add_nuclide('U235', 0.1505368005)
UO2_mat.add_nuclide('U238', 3.868647792)
UO2_mat.add_nuclide('O16', 8.038320323)
UO2_mat.set_density('g/cm3', 10.97)
# обогащение по урану  3.6 и 4% гадолиния
#mixed_with_Gd2O3_mat = openmc.Material(material_id=1, name='mixed_with_Gd2O3_mat', temperature=1027)
#mixed_with_Gd2O3_mat.add_nuclide('U235', 0.1171720456, percent_type='ao')
#mixed_with_Gd2O3_mat.add_nuclide('U238', 3.362402709, percent_type='ao')
#mixed_with_Gd2O3_mat.add_nuclide('O16', 7.303819959, percent_type='ao')
#mixed_with_Gd2O3_mat.add_nuclide('Gd152', 0.0004370424006, percent_type='ao')
#mixed_with_Gd2O3_mat.add_nuclide('Gd154', 0.003764567218, percent_type='ao')
#mixed_with_Gd2O3_mat.add_nuclide('Gd155', 0.03235536051, percent_type='ao')
#mixed_with_Gd2O3_mat.add_nuclide('Gd156', 0.04467730649, percent_type='ao')
#mixed_with_Gd2O3_mat.add_nuclide('Gd157', 0.03399398213, percent_type='ao')
#mixed_with_Gd2O3_mat.add_nuclide('Gd158', 0.05359985427, percent_type='ao')
#mixed_with_Gd2O3_mat.add_nuclide('Gd160', 0.04660386482, percent_type='ao')
#mixed_with_Gd2O3_mat.set_density('g/cm3', 10.8276)

#print(mixed_with_Gd2O3_mat.get_nuclide_atom_densities())

E110_mat=openmc.Material(material_id=2, name='E110_mat')
E110_mat.add_element('Zr', 98.97, percent_type='wo')
E110_mat.add_element('Nb', 1.0, percent_type='wo')
E110_mat.add_element('Hf', 0.03, percent_type='wo')
E110_mat.set_density('g/cm3', 6.4516)

E635_mat=openmc.Material(material_id=3, name='E635_mat')
E635_mat.add_element('Zr', 98.47, percent_type='wo')
E635_mat.add_element('Nb', 1.0, percent_type='wo')
E635_mat.add_element('Fe', 0.50, percent_type='wo')
E635_mat.add_element('Hf', 0.03, percent_type='wo')
E635_mat.set_density('g/cm3', 6.5500)

steel_mat=openmc.Material(material_id=4, name='steel_mat')
steel_mat.add_element('Fe', 69.50, percent_type='wo')
steel_mat.add_element('Cr', 18.0, percent_type='wo')
steel_mat.add_element('Ni', 11.0, percent_type='wo')
steel_mat.add_element('Mn', 1.50, percent_type='wo')
steel_mat.set_density('g/cm3', 7.9)

Dy2O3TiO2_mat=openmc.Material(material_id=5, name='Dy2O3TiO2_mat')
Dy2O3TiO2_mat.add_element('O', 18.0, percent_type='wo')
Dy2O3TiO2_mat.add_element('Ti', 12.0, percent_type='wo')
Dy2O3TiO2_mat.add_element('Dy', 70.0, percent_type='wo')
Dy2O3TiO2_mat.set_density('g/cm3', 5.1)

B4C_mat=openmc.Material(material_id=6,name='B4C_mat')
B4C_mat.add_nuclide('B10', 14.43, percent_type='wo')
B4C_mat.add_nuclide('B11', 63.84, percent_type='wo')
B4C_mat.add_element('C', 21.74, percent_type='wo')
B4C_mat.set_density('g/cm3', 1.8)

water_mat = openmc.Material(material_id=7, name='water_mat', temperature=575)
water_mat.add_element('H', 0.04843, percent_type='ao')
water_mat.add_nuclide('O16', 0.02422, percent_type='ao')
water_mat.add_nuclide('B10', 0.000004794, percent_type='ao')
water_mat.add_nuclide('B11', 0.00001942, percent_type='ao')
water_mat.set_density('g/cm3', 0.7235)
print(water_mat.get_nuclide_atom_densities())



materials=openmc.Materials([UO2_mat, E110_mat, E635_mat, steel_mat, Dy2O3TiO2_mat, B4C_mat, water_mat])
materials.export_to_xml()

class AbstractUO2():
    def __init__(self, enr, density=10.4, temp=1027):
        mat = openmc.Material(material_id=random.randint(100,10000), name=f'UO2_{enr:.1f}', temperature=temp)
        mat.add_element('U', 1.0, enrichment=4.0)
        mat.add_element('O', 2.0)
        mat.set_density('g/cm3', density)
        self.mat = mat

class AbstractUO22():
    def __init__(self, enr_tvegs, density=10.4, temp=1027):
        mat = openmc.Material(material_id=random.randint(10000,20000), name=f'UO2_{enr_tvegs:.1f}', temperature=temp)
        mat.add_element('U', 1.0, enrichment=4.0)
        mat.add_element('O', 2.0)
        mat.set_density('g/cm3', density)
        self.mat = mat


# water_mat=openmc.Material(name='water')
# water_mat.add_nuclide('H1', 2.*0.999885, percent_type='ao')
# water_mat.add_nuclide('H2', 2.*0.000115, percent_type='ao')
# water_mat.add_nuclide('O16', 0.99757, percent_type='ao')
# water_mat.add_nuclide('O17', 0.00038, percent_type='ao')
# water_mat.add_nuclide('O18', 0.00205, percent_type='ao')
# water_mat.set_density('g/cm3', 0.7235)
# water_mat=openmc.model.borated_water(600, density=0.7235, temperature=575)
# UO2_mat=openmc.Material(name='UO2')
# UO2_mat.add_element('U', 1.0,  enrichment=3.7)
# UO2_mat.add_element('O', 2.0)
# UO2_mat.set_density('g/cm3', 10.4)
# UO2_mat.volume=V
# UO2_mat.temperature=1027
# UO2_mat1=openmc.Material(name='UO21')
# UO2_mat1.add_element('U', 1.0,  enrichment=3.6)
# UO2_mat1.add_element('O', 2.0)
# UO2_mat1.set_density('g/cm3', 10.4)
# UO2_mat1.volume=V
# UO2_mat1.temperature=1027
# UO2_mat.depletable=True
# zirconi_mat=openmc.Material()
# zirconi_mat.add_element('Zr', 0.99)
# zirconi_mat.add_element('Nb', 0.01)
# zirconi_mat.set_density('g/cm3', 6.55)
Gd2O3_mat=openmc.Material()
Gd2O3_mat.add_element('Gd', 2.0, percent_type='ao')
Gd2O3_mat.add_element('O', 3.0, percent_type='ao')
Gd2O3_mat.set_density( 'g/cm3', 7.41)
#mixed_with_Gd2O3_mat=openmc.Material.mix_materials(
#   materials=[
#        mat,
#        Gd2O3_mat,
#    ],
#    fracs=[0.96, 0.04],
#    percent_type='vo')
#mixed_with_Gd2O3_mat.depletable=True
#mixed_with_Gd2O3_mat.volume=R**2*pi*350*18*7
#mixed_with_Gd2O3_mat.temperature=1027
helium_mat=openmc.Material(name='Helium')
helium_mat.add_element('He', 1.0)
helium_mat.set_density('g/cm3', 0.0001785)
# water_mat = nmm.Material.from_library(name='Water, Liquid').openmc_material
# water_mat.temperature=575
# cladding_mat1 = nmm.Material.from_library(name='Zircaloy-2', temperature=575).openmc_material
# Nb_mat=openmc.Material()
# Nb_mat.add_element('Nb', 100 )
# Nb_mat.set_density('g/cm3', 8.57)
# cladding_mat=openmc.Material.mix_materials(
#    materials=[
#        cladding_mat1,
#        Nb_mat,
#    ],
#    fracs=[0.99, 0.01],
#    percent_type='vo'
# )
# cladding_mat.temperature=575


# tube_mat=nmm.Material.from_library(name='SS_316L_N_IG').openmc_material
# tube_mat.temperature=575
