import random

import openmc
from openmc.data import NATURAL_ABUNDANCE
import math
from math import pi
import neutronics_material_maker as nmm

# обогащение 3.7

#print(UO2_mat.get_nuclides)
# обогащение по урану  3.6 и 4% гадолиния
#mixed_with_Gd2O3_mat = openmc.Material( name='mixed_with_Gd2O3_mat', temperature=575)
#mixed_with_Gd2O3_mat.add_nuclide('U235', 1.155077423, percent_type='ao')
#mixed_with_Gd2O3_mat.add_nuclide('U238', 30.54000932, percent_type='ao')
#mixed_with_Gd2O3_mat.add_nuclide('O16', 66.33908814, percent_type='ao')
#mixed_with_Gd2O3_mat.add_nuclide('Gd152', 0.003987731444, percent_type='ao')
#mixed_with_Gd2O3_mat.add_nuclide('Gd154', 0.04327557995, percent_type='ao')
#mixed_with_Gd2O3_mat.add_nuclide('Gd155', 0.2938770567, percent_type='ao')
#mixed_with_Gd2O3_mat.add_nuclide('Gd156', 0.4057947471, percent_type='ao')
#mixed_with_Gd2O3_mat.add_nuclide('Gd157', 0.3087603185, percent_type='ao')
#mixed_with_Gd2O3_mat.add_nuclide('Gd158', 0.4868364056, percent_type='ao')
#mixed_with_Gd2O3_mat.add_nuclide('Gd160', 0.4232932785, percent_type='ao')
#mixed_with_Gd2O3_mat.set_density('g/cm3', 10.2279)

#print(mixed_with_Gd2O3_mat.get_nuclide_atom_densities())

E110_mat=openmc.Material( name='E110_mat', temperature=575)
E110_mat.add_element('Zr', 98.97, percent_type='wo')
E110_mat.add_element('Nb', 1.0, percent_type='wo')
E110_mat.add_element('Hf', 0.03, percent_type='wo')
E110_mat.set_density('g/cm3', 6.4516)

E635_mat=openmc.Material( name='E635_mat', temperature=575)
E635_mat.add_element('Zr', 98.47, percent_type='wo')
E635_mat.add_element('Nb', 1.0, percent_type='wo')
E635_mat.add_element('Fe', 0.50, percent_type='wo')
E635_mat.add_element('Hf', 0.03, percent_type='wo')
E635_mat.set_density('g/cm3', 6.5500)
print(E110_mat.get_nuclide_atom_densities())
steel_mat=openmc.Material(material_id=4, name='steel_mat', temperature=575)
steel_mat.add_element('Fe', 69.50, percent_type='wo')
steel_mat.add_element('Cr', 18.0, percent_type='wo')
steel_mat.add_element('Ni', 11.0, percent_type='wo')
steel_mat.add_element('Mn', 1.50, percent_type='wo')
steel_mat.set_density('g/cm3', 7.9)

Dy2O3TiO2_mat=openmc.Material(material_id=5, name='Dy2O3TiO2_mat', temperature=575)
Dy2O3TiO2_mat.add_element('O', 18.0, percent_type='wo')
Dy2O3TiO2_mat.add_element('Ti', 12.0, percent_type='wo')
Dy2O3TiO2_mat.add_element('Dy', 70.0, percent_type='wo')
Dy2O3TiO2_mat.set_density('g/cm3', 5.1)

B4C_mat=openmc.Material(name='B4C_mat', temperature=575)
B4C_mat.add_nuclide('B10', 14.43, percent_type='wo')
B4C_mat.add_nuclide('B11', 63.84, percent_type='wo')
B4C_mat.add_nuclide('C0', 21.74, percent_type='wo')
B4C_mat.set_density('g/cm3', 1.8)



#water_mat = openmc.Material( name='water_mat', temperature=575)
#water_mat.add_element('H', 0.04843, percent_type='ao')
#water_mat.add_nuclide('O16', 0.02422, percent_type='ao')
#water_mat.add_nuclide('B10', 0.000004794, percent_type='ao')
#water_mat.add_nuclide('B11', 0.00001942, percent_type='ao')
#water_mat.set_density('g/cm3', 0.7235)
#print(water_mat.get_nuclide_atom_densities())




class AbstractUO2():
    def __init__(self, enr, density=10.2605):
        mat = openmc.Material(material_id=random.randint(100,10000), name=f'UO2_{enr:.1f}', temperature=1027)
        mat.add_element('U', 1.0,  percent_type='ao')
        mat.add_nuclide('O16', 2.0, percent_type='ao')
        mat.set_density('g/cm3', density)
        self.mat = mat


UO2_37_mat=openmc.Material(temperature=1027)
UO2_37_mat.add_element('U', 1.0, enrichment=3.7, percent_type='ao')
UO2_37_mat.add_element('O', 2.0, percent_type='ao')
UO2_37_mat.set_density('g/cm3', 10.35)
#print(UO2_37_mat.get_nuclide_atom_densities())

UO2_36_mat=openmc.Material(temperature=575)
UO2_36_mat.add_element('U', 1.0, enrichment=3.6, percent_type='ao')
UO2_36_mat.add_element('O', 2.0, percent_type='ao')
UO2_36_mat.set_density('g/cm3', 9.61)
#print(UO2_36_mat.get_nuclide_atom_densities())

water_mat=openmc.model.borated_water(1208,  density=0.7235)
water_mat.temperature=575
#water_mat=openmc.Material(name='water_mat', temperature=575)
#water_mat.add_element('H', 66.63986762, percent_type='ao')
#water_mat.add_nuclide('O16', 33.32681383, percent_type='ao')
#water_mat.add_nuclide('B10', 0.006596562572, percent_type='ao')
#water_mat.add_nuclide('B11', 0.02672199523 , percent_type='ao')
#water_mat.set_density('g/cm3',0.7235)

Gd2O3_mat=openmc.Material(temperature=575)
Gd2O3_mat.add_element('Gd', 2.0, percent_type='ao')
Gd2O3_mat.add_nuclide('O16', 3.0, percent_type='ao')
Gd2O3_mat.set_density( 'g/cm3', 7.95)

UO22_mat = openmc.Material.mix_materials(
            materials=[
                UO2_36_mat,
                Gd2O3_mat,
            ],
            fracs=[0.96, 0.04],
            percent_type='wo')
UO22_mat.temperature=575
print(UO22_mat.get_nuclide_atom_densities())
#print(UO22_mat.density)
#print(UO22_mat.get_nuclide_atom_densities())
helium_mat=openmc.Material(name='Helium')
helium_mat.add_element('He', 1.0)
helium_mat.set_density('g/cm3', 0.0001785)


#print(UO2_mat1.get_nuclides)
