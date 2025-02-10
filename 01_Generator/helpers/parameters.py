import json
import numpy as np

class DatasetParameters():
    def __init__(self, json_file_path):
        json_data = self.read_json_file(json_file_path)

        self.raw_dict = json_data

        self.output_dir = json_data.get('output_dir')
        self.name = json_data.get('name')
        
        # Dataset-options
        self.dataset_opts = json_data.get('dataset-options')
        
        # Odometry
        self.odometry = json_data.get('odometry')

        # Intra loop closure
        self.lc_intra = json_data.get('intra-loop-closure')

        # Indirect inter loop closure
        self.lc_inter_indirect = json_data.get('inter-indirect-loop-closure')

        # Direct inter loop closure
        self.lc_inter_direct = json_data.get('inter-direct-loop-closure')

        # Landmarks
        self.landmarks = json_data.get('landmarks')

        # Sigmas
        self.sigmas = json_data.get('sigmas')
     
        # Limits
        self.limits = json_data.get('limits')

    # @property
    # def raw_dict(self):
    #     return self._raw_dict
    # @property
    # def output_dir(self):
    #     return self._output_dir
    # @output_dir.setter
    # def output_dir(self, value):
    #     if not isinstance(value, str):
    #         raise ValueError("Name must be a string")
    #     self._output_dir = value

    # @property
    # def name(self):
    #     return self._name
    # @name.setter
    # def name(self, value):
    #     if not isinstance(value, str):
    #         raise ValueError("Name must be a string")
    #     self._name = value

    def __str__(self):
        output  = f"----------------------------------\n"
        output += f"-----  Dataset Parameters :  -----\n"
        output += f"----------------------------------\n\n"
        output += f"Dataset name : {self.name}\n"
        output += f"Output directory : {self.output_dir}\n"
        output += f"\n"

        if self.dataset_opts is not None:
            output += f"Dataset-options :\n"
            output += f"-----------------\n"
            output += f"Number of reapeats : {self.dataset_opts['repeats']}\n"
            output += f"Number of poses : {self.dataset_opts['number_poses']}\n"
            output += f"Number of robots : {self.dataset_opts['number_robots']}\n"
            output += f"Initialization type : {self.dataset_opts['initialization_type']}\n"
            output += f"\n"

        if self.landmarks is not None:
            output += f"Landmarks :\n"
            output += f"----------\n"
            output += f"Number of landmarks : {self.landmarks['number']}\n"
            output += f"Seed : {self.landmarks['seed']}\n"
            output += f"Probability : {self.landmarks['probability']}\n"
            output += f"\n"
        
        if self.odometry is not None:
            output += f"Odometry :\n"
            output += f"----------\n"
            output += f"Displacement probabilities : {self.odometry['odom_probs']}\n"
            output += f"\n"

        if self.lc_intra is not None:
            output += f"Loop closure - Intra :\n"
            output += f"----------------------\n"
            output += f"Distance threshold : {self.lc_intra['distance_threshold']}\n"
            output += f"Index threshold : {self.lc_intra['index_threshold']}\n"
            output += f"Probability : {self.lc_intra['probability']}\n"
            output += f"\n"

        if self.lc_inter_indirect is not None:
            output += f"Loop closure - Inter - Indirect :\n"
            output += f"---------------------------------\n"
            output += f"Distance threshold : {self.lc_inter_indirect['distance_threshold']}\n"
            output += f"Index threshold : {self.lc_inter_indirect['index_threshold']}\n"
            output += f"Probability : {self.lc_inter_indirect['probability']}\n"
            output += f"\n"

        if self.lc_inter_direct is not None:
            output += f"Loop closure - Inter - Direct :\n"
            output += f"-------------------------------\n"
            for key in self.lc_inter_direct.keys():
                output += key + ' : ' + str(self.lc_inter_direct[key]) + "\n"
            output += f"\n"

        if self.sigmas is not None:
            output += f"Sigmas :\n"
            output += f"--------\n"
            output += f"Initialization : {self.sigmas['initialization']}\n"
            output += f"\n"
            output += f"Prior : {self.sigmas['prior']}\n"
            output += f"Robot Zero Prior : {self.sigmas['robot_zero_prior']}\n"
            output += f"\n"
            output += f"Odometry : {self.sigmas['odom']}\n"
            output += f"\n"
            output += f"Loop Closure [Intra] : {self.sigmas['lc_intra']}\n"
            output += f"Loop Closure [Inter-Indirect] : {self.sigmas['lc_inter_indirect']}\n"
            output += f"Loop Closure [Inter-Direct-Pose] : {self.sigmas['lc_inter_direct_pose']}\n"
            output += f"Loop Closure [Inter-Direct-Range] : {self.sigmas['lc_inter_direct_range']}\n"
            output += f"\n"
            output += f"Landmarks : {self.sigmas['landmarks']}\n"
            output += f"\n"
        
        if self.limits is not None:
            output += f"Limits :\n"
            output += f"--------\n"
            output += f"X : {self.limits['x']}\n"
            output += f"Y : {self.limits['y']}\n"
            output += f"Z : {self.limits['z']}\n"
        
        return output
    
    def read_json_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from the file '{file_path}'.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

class MESAParameters:
    def __init__(self):
        self.ComputeZMethod = {'OPTIMIZE':0,
                                'INTERPOLATE_SPLIT':1,
                                'INTERPOLATE_SLERP':2}
        self.DualComputeTarget = {'SHARED_ESTIMATE':0,
                                    'OTHER_ESTIMATE':1,
                                    'UNWEIGHTED_SLERP':2,
                                    'CHOUDHARY_TARGET':3}
        self._pseudo_sync_beta = False
        self._convergence_threshold = 1e-4

        self._beta_init = 10.0
        self._beta_multipliers_increase = 1.0
        self._prior_shared_vars_on_indep_solve = False
        self._shared_var_prior_sigmas = np.array([2,2,2,1e2,1e2,1e2])
        self._z_compute_method = self.ComputeZMethod['OPTIMIZE']
        self._weight_z_compute = False
        self._dual_compute_target = self.DualComputeTarget['SHARED_ESTIMATE']

    @property
    def pseudo_sync_beta(self):
        return self._pseudo_sync_beta

    @property
    def convergence_threshold(self):
        return self._convergence_threshold

    @property
    def beta_init(self):
        return self._beta_init
    @beta_init.setter
    def beta_init(self, value):
        if isinstance(value, float):
            self._beta_init = value
        else:
            raise ValueError("ID must be a float")

    @property
    def beta_multipliers_increase(self):
        return self._beta_multipliers_increase
    @beta_multipliers_increase.setter
    def beta_multipliers_increase(self, value):
        if isinstance(value, float):
            self._beta_multipliers_increase = value
        else:
            raise ValueError("ID must be a float")

    @property
    def prior_shared_vars_on_indep_solve(self):
        return self._prior_shared_vars_on_indep_solve
    @prior_shared_vars_on_indep_solve.setter
    def prior_shared_vars_on_indep_solve(self, value):
        if isinstance(value, bool):
            self._prior_shared_vars_on_indep_solve = value
        else:
            raise ValueError("ID must be a boolean")

    @property
    def shared_var_prior_sigmas(self):
        return self._shared_var_prior_sigmas
    @shared_var_prior_sigmas.setter
    def shared_var_prior_sigmas(self, value):
        if isinstance(value, np.ndarray):
            self._shared_var_prior_sigmas = value
        else:
            raise ValueError("ID must be a float")

    @property
    def z_compute_method(self):
        if self._z_compute_method == self.ComputeZMethod['OPTIMIZE']:
            return 'OPTIMIZE'
        elif self._z_compute_method == self.ComputeZMethod['INTERPOLATE_SPLIT']:
            return 'INTERPOLATE_SPLIT'
        elif self._z_compute_method == self.ComputeZMethod['INTERPOLATE_SLERP']:
            return 'INTERPOLATE_SLERP'
    @z_compute_method.setter
    def z_compute_method(self, value):
        if isinstance(value, str):
                if value == 'OPTIMIZE':
                        self._z_compute_method = self.ComputeZMethod['OPTIMIZE']
                elif value == 'INTERPOLATE_SPLIT':
                        self._z_compute_method = self.ComputeZMethod['INTERPOLATE_SPLIT']
                elif value == 'INTERPOLATE_SLERP':
                        self._z_compute_method = self.ComputeZMethod['INTERPOLATE_SLERP'] 
        else:
                raise ValueError("ID must be a string")

    @property
    def weight_z_compute(self):
        return self._weight_z_compute
    @weight_z_compute.setter
    def weight_z_compute(self, value):
        if isinstance(value, bool):
                self._weight_z_compute = value
        else:
                raise ValueError("ID must be a boolean")

    @property
    def dual_compute_target(self):
        if self._dual_compute_target == self.DualComputeTarget['SHARED_ESTIMATE']:
                return 'SHARED_ESTIMATE'
        elif self._dual_compute_target == self.DualComputeTarget['OTHER_ESTIMATE']:
                return 'OTHER_ESTIMATE'
        elif self._dual_compute_target == self.DualComputeTarget['UNWEIGHTED_SLERP']:
                return 'UNWEIGHTED_SLERP'
        elif self._dual_compute_target == self.DualComputeTarget['CHOUDHARY_TARGET']:
                return 'CHOUDHARY_TARGET'
    @dual_compute_target.setter
    def dual_compute_target(self, value):
        if isinstance(value, str):
                if value == 'SHARED_ESTIMATE':
                        self._dual_compute_target = self.DualComputeTarget['SHARED_ESTIMATE']
                elif value == 'OTHER_ESTIMATE':
                        self._dual_compute_target = self.DualComputeTarget['OTHER_ESTIMATE']
                elif value == 'UNWEIGHTED_SLERP':
                        self._dual_compute_target = self.DualComputeTarget['UNWEIGHTED_SLERP']
                elif value == 'CHOUDHARY_TARGET':
                        self._dual_compute_target = self.DualComputeTarget['CHOUDHARY_TARGET']
        else:
                raise ValueError("ID must be a string")

    def __str__(self):
        output = f"*****  MESA Parameters :  *****\n"
        output += f"beta_init : {self._beta_init}\n"
        output += f"beta_multipliers_increase : {self._beta_multipliers_increase}\n"
        output += f"prior_shared_vars_on_indep_solve : {self._prior_shared_vars_on_indep_solve}\n"
        if self._z_compute_method == self.ComputeZMethod['OPTIMIZE']:
                method = 'OPTIMIZE'
        elif self._z_compute_method == self.ComputeZMethod['INTERPOLATE_SPLIT']:
                method = 'INTERPOLATE_SPLIT'
        elif self._z_compute_method == self.ComputeZMethod['INTERPOLATE_SLERP']:
                method = 'INTERPOLATE_SLERP'
        output += f"z_compute_method : {method}\n"
        output += f"weight_z_compute : {self._weight_z_compute}\n"
        if self._dual_compute_target == self.DualComputeTarget['SHARED_ESTIMATE']:
                target = 'SHARED_ESTIMATE'
        elif self._dual_compute_target == self.DualComputeTarget['OTHER_ESTIMATE']:
                target = 'OTHER_ESTIMATE'
        elif self._dual_compute_target == self.DualComputeTarget['UNWEIGHTED_SLERP']:
                target = 'UNWEIGHTED_SLERP'
        elif self._dual_compute_target == self.DualComputeTarget['CHOUDHARY_TARGET']:
                target = 'CHOUDHARY_TARGET'
        output += f"dual_compute_target : {target}\n"
        return output

if __name__ == '__main__':
    # Dataset Parameters
    file_path = '/home/workspace/configs/default.json'
    Params = DatasetParameters(file_path)
    print(Params)
    # print(Params)

    # MESA Parameters
    # mesa_params = MESAParams()
    # print(mesa_params)