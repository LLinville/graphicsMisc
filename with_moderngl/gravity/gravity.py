import os

import moderngl_window as mglw


class GravitySim(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "ModernGL Gravity"
    window_size = (1280, 720)
    aspect_ratio = 16 / 9
    resizable = True
    samples = 4

    resource_dir = os.path.normpath(os.path.join(__file__, '../../data'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.forces = self.ctx.program(
            vertex_shader='''
                    #version 330 core
                    
                    struct Particle{
                        vec2 pos;
                        vec2 vel;
                        vec2 acc;
                    };
                    
                    layout (std140, binding=0) buffer ParticleBuffer{
                        Particle particles[];
                    };
    
                    uniform vec2 n_particles;
    
                    in Particle in_particle;
    
                    out Particle out_particle;
                    
                    float force(vec2 p_one, vec2 p_two){
                        vec2 diff = p_two - p_one;
                        vec2 dist_squared = dot(dist, dist) + 0.001;
                        return diff / dist_squared;
                    }
    
                    void main() {
                        vec2 total_force = vec2(0,0);
                        for(int i=0; i < n_particles; i++){
                            total_force += force(in_pos, particles[i].pos)
                        }
                        out_pos = in_pos * 2.0 - in_prev + Acc;
                        out_prev = in_pos;
                    }
                ''',
            varyings=['out_particle']
        )

        # self.apply_forces = self.ctx.program(
        #     vertex_shader='''
        #                     #version 330
        #
        #                     uniform vec2 n_particles;
        #
        #                     in vec2 in_pos;
        #
        #                     out vec2 out_acc;
        #
        #                     void main() {
        #                         out_pos = in_pos * 2.0 - in_prev + Acc;
        #                         out_prev = in_pos;
        #                     }
        #                 ''',
        #     varyings=['out_pos']
        # )

        self.display = self.ctx.program(
            vertex_shader='''
                        #version 330

                        in vec2 in_vert;

                        void main() {
                            gl_Position = vec4(in_vert, 0.0, 1.0);
                        }
                    ''',
            fragment_shader='''
                        #version 330

                        out vec4 f_color;

                        void main() {
                            f_color = vec4(0.30, 0.50, 1.00, 1.0);
                        }
                    ''',
        )

        self.forces['n_particles'].value = 100

    @classmethod
    def run(cls):
        mglw.run_window_config(cls)
