import openmc
import openmc.deplete
import sys
import openmc.model
from openmc import stats
import neutronics_material_maker as nmm
from mat import water_mat,  AbstractUO2, Gd2O3_mat, helium_mat, E110_mat, E635_mat, steel_mat, Dy2O3TiO2_mat, B4C_mat, AbstractUO2
#openmc.config['cross_sections']='/home/ann/PycharmProjects/1000/library/jeff33 (1)/jeff-3.3-hdf5/cross_sections.xml'
openmc.config['cross_sections']='/home/ann/PycharmProjects/library_/endfb71/endfb-vii.1-hdf5/cross_sections.xml'


import matplotlib.pyplot as plt
from core import get_TVS_universe
from params import GeometryParams


import numpy as np
if __name__ == "__main__":
    top_surf=openmc.ZPlane(z0=186.5)
    bottom_surf=openmc.ZPlane(z0=-186.5)
    top_surf.boundary_type='reflective'
    bottom_surf.boundary_type='reflective'

    mats=[]
    mats_id=[]
    TVS1, mats1=get_TVS_universe(3.0, 2.4 , False, 1, 0,1.6, 0)
    mats+=mats1
    mats_id=[mat.id for mat in mats]
    TVS2, mats2 =get_TVS_universe(1.3, 0, False, 0, 0, 0,  verbose=False)
    for mat in mats2:
        if mat.id not in mats_id:
            mats.append(mat)
            mats_id.append(mat.id)
    materials = openmc.Materials([ Gd2O3_mat, helium_mat, E110_mat, E635_mat, steel_mat, Dy2O3TiO2_mat, B4C_mat]+mats)

    all_water2_cell = openmc.Cell(fill=water_mat)
    water2_universe = openmc.Universe(cells=[all_water2_cell, ])
    core_lat = openmc.HexLattice()
    core_lat.center = (0.0, 0.0)
    core_lat.pitch = [23.6]
    core_lat.outer = water2_universe
    core_lat.orientation = 'y'
    outer_ring = [TVS1] * 6
    inner2_ring = [TVS2]
    core_lat.universes = [outer_ring, inner2_ring]
    outer2_radius = 100
    outer2_surf = openmc.ZCylinder(r=outer2_radius, boundary_type='reflective')
    core_cell = openmc.Cell(fill=core_lat, region=-outer2_surf & +bottom_surf & -top_surf)

    materials.export_to_xml()
    params = GeometryParams()
    # print(universe.get_all_materials())
    geometry=openmc.Geometry()
    geometry.root_universe=openmc.Universe(0, cells=[core_cell,])
    settings=openmc.Settings()
    settings.temperature={'method': 'interpolation'}
    uniform_dist = stats.Box([-10, -10, -350 / 2], [10, 10, 350 / 2], only_fissionable=True)
    source = openmc.source.Source(space=uniform_dist)
    source.time = stats.Uniform(0, 1)
    settings.source = source
    flux_tally = openmc.Tally(name='flux')
    flux_tally.scores = ['flux']
    U_tally = openmc.Tally(name='fuel')
    U_tally.scores = ['fission', 'total', 'absorption', 'elastic', 'scatter', 'decay-rate']
    U_tally.nuclides = ['U235', 'U238', 'O16', 'H1']
    settings.batches = 100
    settings.particles = 6000
    settings.inactive = 10
    #power = (3000.0e6)/163  # watts
    #model = openmc.Model(geometry, materials, settings)
    #chain_file = '/home/ann/PycharmProjects/1000/library/chain_endfb71_pwr.xml'
    #operator = openmc.deplete.CoupledOperator(model, chain_file)
    #timesteps = [ (2,'MWd/kg'), (4,'MWd/kg'), (6,'MWd/kg'), (8,'MWd/kg'), (10,'MWd/kg'), (12,'MWd/kg'), (14,'MWd/kg'), (15,'MWd/kg'), (20,'MWd/kg'), (40, 'MWd/kg')]  # days
    #integrator=openmc.deplete.PredictorIntegrator(operator, timesteps,  power_density=108.0e6, timestep_units='MWd/kg')


    #openmc.deplete.CECMIntegrator(op, timesteps, power, timestep_units='d').integrate()
    #results = openmc.deplete.Results("depletion_results.h5")
    #time, keff = results.get_keff()

    #settings.run_mode = 'fixed source'
    #cecm = openmc.deplete.CECMIntegrator(operator, dt, power)
    #cecm.integrate()
    #source.strength = 18e0



    #plots = openmc.Plots(plots)
    colors = {water_mat: (32, 178, 170)}
    color_data = dict(color_by='material', colors=colors)
    width = np.array([params.TVS_edge_length * 5.1, params.TVS_edge_length * 5.1, ])
    scale = 5.1 / 2
    fig, ax = plt.subplots(2, 2)

    geometry.root_universe.plot(width=width / scale, pixels=(1000, 1000), basis='xz', **color_data,
                  origin=(0, 0, GeometryParams.tvel_heigh / 2 - 1), axes=ax[0][0])
    geometry.root_universe.plot(width=width / scale, pixels=(1000, 1000), basis='xz', **color_data, origin=(0, 0, 0), axes=ax[1][1])
    geometry.root_universe.plot(width=width / scale, pixels=(1000, 1000), basis='xz', **color_data,
                  origin=(0, 0, -GeometryParams.tvel_heigh / 2 + 1),
                  axes=ax[0][1])
    geometry.root_universe.plot(width=width / scale, pixels=(1000, 1000), basis='xy', **color_data, origin=(0, 0, 0), axes=ax[1][0])
    plt.savefig('plots/geometry.jpg')

    # ...and by openmc.Plots
    plots = [openmc.Plot(), openmc.Plot(), openmc.Plot(), openmc.Plot(), ]
    for i in range(4):
        plots[i].width = width
        plots[i].pixels = (2000, 2000)
        plots[i].basis = 'xz'
        plots[i].color_by = 'material'
        plots[i].colors = colors
    plots[0].origin = (0, 0, GeometryParams.tvel_heigh / 2 - 1)
    plots[2].origin = (0, 0, -GeometryParams.tvel_heigh / 2 - 1)
    plots[-1].basis = 'xy'

    plots = openmc.Plots(plots)

    tallies_file=openmc.Tallies([flux_tally, U_tally])
    tallies_file.export_to_xml('xmlki/tallies.xml')


    plots.export_to_xml('xmlki/plots.xml')
    settings.export_to_xml('xmlki/settings.xml')
    geometry.export_to_xml('geometry.xml')
    #model.export_to_xml('model.xml')
    openmc.plot_geometry()
    openmc.run()
