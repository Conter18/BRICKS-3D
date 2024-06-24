#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
in vec3 normal;
in vec3 fragPos;

struct Light {
    vec3 position;
    vec3 Ia;  // Ambient light intensity
    vec3 Id;  // Diffuse light intensity
    vec3 Is;  // Specular light intensity
};  

uniform Light light;
uniform sampler2D u_texture_0;
uniform vec3 camPos;

vec3 getLight(vec3 color, vec3 norm, vec3 fragPos) {
    vec3 Normal = normalize(normal);

    // Ambient light
    vec3 ambient = light.Ia * color;

    // Diffuse light
    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = light.Id * diff * color;

    // Specular light
    vec3 viewDir = normalize(-fragPos);  // Assume the viewer is at the origin
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
    vec3 specular = light.Is * spec;

    return ambient + diffuse + specular;
}

void main() {
    vec3 norm = normalize(normal);
    vec3 color = texture(u_texture_0, uv_0).rgb;
    color = getLight(color, norm, fragPos);
    fragColor = vec4(color, 1.0);
}
