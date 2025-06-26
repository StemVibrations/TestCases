import numpy as np

from stem.model import Model
from stem.default_materials import DefaultMaterial
from stem.soil_material import OnePhaseSoil, LinearElasticSoil, SoilMaterial, SaturatedBelowPhreaticLevelLaw
from stem.structural_material import ElasticSpringDamper, NodalConcentrated
from stem.boundary import DisplacementConstraint
from stem.load import MovingLoad
from stem.solver import AnalysisType, SolutionType, TimeIntegration, DisplacementConvergenceCriteria, \
    StressInitialisationType, SolverSettings, Problem, LinearNewtonRaphsonStrategy
from stem.output import NodalOutput, Output, VtkOutputParameters, JsonOutputParameters
from stem.stem import Stem


def run_analysis(speed, output_dir, vtk):


    ndim = 3
    model = Model(ndim)
    model.extrusion_length = 60
    time_step = 0.05
    total_time = 60 / speed
    # round total_time to multiple of time_step
    total_time = np.floor(total_time / time_step) * time_step


    # Specify material model
    # Linear elastic drained soil with a Density of 2650, a Young's modulus of 30e6,
    # a Poisson ratio of 0.2 & a Porosity of 0.3 is specified.
    DENSITY_SOLID = 2650
    POROSITY = 0.23
    YOUNG_MODULUS = 438.7e6
    POISSON_RATIO = 0.3
    soil_formulation1 = OnePhaseSoil(ndim, IS_DRAINED=True, DENSITY_SOLID=DENSITY_SOLID, POROSITY=POROSITY)
    constitutive_law1 = LinearElasticSoil(YOUNG_MODULUS=YOUNG_MODULUS, POISSON_RATIO=POISSON_RATIO)
    retention_parameters1 = SaturatedBelowPhreaticLevelLaw()
    material1 = SoilMaterial("soil_1", soil_formulation1, constitutive_law1, retention_parameters1)

    DENSITY_SOLID = 2650
    POROSITY = 0.45
    YOUNG_MODULUS = 45.2e6
    POISSON_RATIO = 0.43
    soil_formulation2 = OnePhaseSoil(ndim, IS_DRAINED=True, DENSITY_SOLID=DENSITY_SOLID, POROSITY=POROSITY)
    constitutive_law2 = LinearElasticSoil(YOUNG_MODULUS=YOUNG_MODULUS, POISSON_RATIO=POISSON_RATIO)
    retention_parameters2 = SaturatedBelowPhreaticLevelLaw()
    material2 = SoilMaterial("soil_2", soil_formulation2, constitutive_law2, retention_parameters2)

    DENSITY_SOLID = 2650
    POROSITY = 0.59
    YOUNG_MODULUS = 18.3e6
    POISSON_RATIO = 0.495
    soil_formulation3 = OnePhaseSoil(ndim, IS_DRAINED=True, DENSITY_SOLID=DENSITY_SOLID, POROSITY=POROSITY)
    constitutive_law3 = LinearElasticSoil(YOUNG_MODULUS=YOUNG_MODULUS, POISSON_RATIO=POISSON_RATIO)
    retention_parameters3 = SaturatedBelowPhreaticLevelLaw()
    material3 = SoilMaterial("soil_3", soil_formulation3, constitutive_law3, retention_parameters3)

    DENSITY_SOLID = 2650
    POROSITY = 0.31
    YOUNG_MODULUS = 168.3e6
    POISSON_RATIO = 0.495
    soil_formulation4 = OnePhaseSoil(ndim, IS_DRAINED=True, DENSITY_SOLID=DENSITY_SOLID, POROSITY=POROSITY)
    constitutive_law4 = LinearElasticSoil(YOUNG_MODULUS=YOUNG_MODULUS, POISSON_RATIO=POISSON_RATIO)
    retention_parameters4 = SaturatedBelowPhreaticLevelLaw()
    material4 = SoilMaterial("soil_4", soil_formulation4, constitutive_law4, retention_parameters4)

    DENSITY_SOLID = 2650
    POROSITY = 0.25
    YOUNG_MODULUS = 100e6
    POISSON_RATIO = 0.3
    soil_formulation5 = OnePhaseSoil(ndim, IS_DRAINED=True, DENSITY_SOLID=DENSITY_SOLID, POROSITY=POROSITY)
    constitutive_law5 = LinearElasticSoil(YOUNG_MODULUS=YOUNG_MODULUS, POISSON_RATIO=POISSON_RATIO)
    retention_parameters5 = SaturatedBelowPhreaticLevelLaw()
    ballast = SoilMaterial("ballast", soil_formulation5, constitutive_law5, retention_parameters5)

    node_1 = (0.0, 0.0, 0.0)
    node_2 = (20.0, 0.0, 0.0)
    node_3 = (0.0, 5.0, 0.0)
    node_4 = (20.0, 5.0, 0.0)
    node_5 = (0.0, 5.5, 0.0)
    node_6 = (20.0, 5.5, 0.0)
    node_7 = (0.0, 6.4, 0.0)
    node_8 = (20.0, 6.4, 0.0)
    node_9 = (0.0, 6.8, 0.0)
    node_10 = (20.0, 6.8, 0.0)
    node_11 = (0.0, 7.1, 0.0)
    node_12 = (2.5, 7.1, 0.0)
    node_13 = (3, 6.8, 0.0)


    # Specify the coordinates for the column: x:5m x y:1m
    layer1_coordinates = [node_1, node_2, node_4, node_3]
    layer2_coordinates = [node_3, node_4, node_6, node_5]
    layer3_coordinates = [node_5, node_6, node_8, node_7]
    layer4_coordinates = [node_7, node_8, node_10, node_9]
    layer5_coordinates = [node_9, node_13, node_12, node_11]

    # Create the soil layer
    model.add_soil_layer_by_coordinates(layer1_coordinates, material4, "soil_4")
    model.add_soil_layer_by_coordinates(layer2_coordinates, material3, "soil_3")
    model.add_soil_layer_by_coordinates(layer3_coordinates, material2, "soil_2")
    model.add_soil_layer_by_coordinates(layer4_coordinates, material1, "soil_1")
    model.add_soil_layer_by_coordinates(layer5_coordinates, ballast, "ballast")

    # add the track
    rail_parameters = DefaultMaterial.Rail_60E1_3D.value.material_parameters
    rail_pad_parameters = ElasticSpringDamper(NODAL_DISPLACEMENT_STIFFNESS=[1, 6e8, 1],
                                                NODAL_ROTATIONAL_STIFFNESS=[0, 0, 0],
                                                NODAL_DAMPING_COEFFICIENT=[1, 2.5e5, 1],
                                                NODAL_ROTATIONAL_DAMPING_COEFFICIENT=[0, 0, 0])
    sleeper_parameters = NodalConcentrated(NODAL_DISPLACEMENT_STIFFNESS=[0, 0, 0],
                                            NODAL_MASS=477/2,
                                            NODAL_DAMPING_COEFFICIENT=[0, 0, 0])

    origin_point = np.array([0.75, 7.1, 0.0])
    direction_vector = np.array([0, 0, 1])
    rail_pad_thickness = 0.025

    # create a straight track with rails, sleepers and rail pads
    model.generate_straight_track(0.6, 101, rail_parameters, sleeper_parameters, rail_pad_parameters, rail_pad_thickness,
                                  origin_point, direction_vector, "rail_track_1")

    moving_load = MovingLoad(load=[0.0, -10000.0, 0.0],
                                direction=[1, 1, 1],
                                velocity=speed,
                                origin=[0.75, 7.1 + rail_pad_thickness, 0.0],
                                offset=0.0)

    model.add_load_on_line_model_part("rail_track_1", moving_load, "moving_load")

    # model.show_geometry(show_surface_ids=True, show_point_ids=True)

    # Define boundary conditions
    no_displacement_parameters = DisplacementConstraint(active=[True, True, True],
                                                        is_fixed=[True, True, True],
                                                        value=[0, 0, 0])
    roller_displacement_parameters = DisplacementConstraint(active=[True, False, True],
                                                            is_fixed=[True, False, True],
                                                            value=[0, 0, 0])

    # Add boundary conditions to the model (geometry ids are shown in the show_geometry)
    model.add_boundary_condition_on_plane([(0, 0, 0), (20, 0, 0), (0, 0, 60)], no_displacement_parameters, "bottom")
    model.add_boundary_condition_on_plane([(0, 0, 0), (20, 0, 0), (0, 7.1, 0)], roller_displacement_parameters, "front")
    model.add_boundary_condition_on_plane([(0, 0, 60), (20, 0, 60), (0, 7.1, 60)], roller_displacement_parameters, "back")
    model.add_boundary_condition_on_plane([(0, 0, 0), (0, 7.1, 0), (0, 0, 60)], roller_displacement_parameters, "left")
    model.add_boundary_condition_on_plane([(20, 0, 0), (20, 7.1, 0), (20, 0, 60)], roller_displacement_parameters, "right")


    # Set up solver settings
    analysis_type = AnalysisType.MECHANICAL
    solution_type = SolutionType.DYNAMIC
    # Set up start and end time of calculation, time step and etc
    time_integration = TimeIntegration(start_time=0.0,
                                        end_time=total_time,
                                        delta_time=time_step,
                                        reduction_factor=1.0,
                                        increase_factor=1.0,
                                        max_delta_time_factor=1000)
    convergence_criterion = DisplacementConvergenceCriteria(displacement_relative_tolerance=1.0e-4,
                                                            displacement_absolute_tolerance=1.0e-12)

    stress_initialisation_type = StressInitialisationType.NONE
    strategy = LinearNewtonRaphsonStrategy()

    solver_settings = SolverSettings(analysis_type=analysis_type,
                                        solution_type=solution_type,
                                        stress_initialisation_type=stress_initialisation_type,
                                        time_integration=time_integration,
                                        is_stiffness_matrix_constant=True,
                                        are_mass_and_damping_constant=True,
                                        convergence_criteria=convergence_criterion,
                                        strategy_type=strategy,
                                        rayleigh_k=0.0002,
                                        rayleigh_m=0.6)

    # Set up problem data
    problem = Problem(problem_name="test_moving_load_on_track_on_soil", number_of_threads=16, settings=solver_settings)
    model.project_parameters = problem

    # Define the results to be written to the output file

    # Nodal results
    nodal_results = [NodalOutput.DISPLACEMENT, NodalOutput.VELOCITY, NodalOutput.ACCELERATION]
    # Gauss point results
    gauss_point_results = []

    # Define the output process

    vtk_output_process = Output(part_name="porous_computational_model_part",
                                output_name="vtk_output",
                                output_dir="output",
                                output_parameters=VtkOutputParameters(file_format="binary",
                                                                        output_interval=1,
                                                                        nodal_results=nodal_results,
                                                                        gauss_point_results=gauss_point_results,
                                                                        output_control_type="step"))

    if vtk:
        model.output_settings = [vtk_output_process]
    else:
        model.output_settings = []


    desired_output_points = [
                            (0.75, 7.1, 30),
                            (2.5, 7.1, 30),
                            ]


    model.add_output_settings_by_coordinates(
        part_name="subset_outputs",
        output_dir=output_dir,
        output_name="json_output",
        coordinates=desired_output_points,
        output_parameters=JsonOutputParameters(
            output_interval=time_step,
            nodal_results=nodal_results,
            gauss_point_results=gauss_point_results
        )
    )

    # Set mesh size
    # --------------------------------
    model.set_mesh_size(element_size=0.5)

    # Write KRATOS input files
    # --------------------------------
    stem = Stem(model, output_dir)
    stem.write_all_input_files()

    # Run Kratos calculation
    # --------------------------------
    stem.run_calculation()


if __name__ == "__main__":
    speed = 120
    run_analysis(speed=speed, output_dir=f"results_{speed}")

