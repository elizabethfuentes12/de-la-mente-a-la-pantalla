
# generative model SD

upscaler =  dict (
    image_uri = '763104351884.dkr.ecr.us-west-2.amazonaws.com/huggingface-pytorch-inference:1.10.2-transformers4.17.0-gpu-py38-cu113-ubuntu20.04',
    model_uri = 's3://jumpstart-cache-prod-us-west-2/stabilityai-infer/prepack/v1.0.0/infer-prepack-model-txt2img-stabilityai-stable-diffusion-v2-1-base.tar.gz',
    s3_path = 'inferences',
    instance_type= 'ml.p3.2xlarge',
    instance_count=1,
    invocation_per_instance=1
)

