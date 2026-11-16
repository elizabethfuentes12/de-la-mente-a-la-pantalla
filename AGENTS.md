# AGENTS.md

## What this is
"De la mente a la pantalla": a CDK (Python) app that deploys an Amazon Lex V2 bot which takes a prompt in any language, translates it with Amazon Translate and generates an image with a Stable Diffusion 2.1 endpoint on Amazon SageMaker; images are served through S3 + CloudFront, with a React front end authenticated with Cognito. Region: us-west-2.

## Structure (all under `cool-image-bot/`)
- `app.py` → `cool_image_bot/cool_image_bot_stack.py` wires everything.
- `lambdas/project_lambdas.py` – `cool_image_hook` (Lex fulfillment: translate + SageMaker invoke + save PNG to S3) and `list_bots`. Code in `lambdas/code/*`.
- `layers/project_layers.py` – `Pillow` (`layers/pil.zip`, Pillow 12.2.0 for python3.13 x86_64), `bs4_requests` (pure Python, unused by the current functions). `layers/common/python/` is a small utils layer.
- `sagemaker/` – Model / EndpointConfig / Endpoint for SD 2.1 (`config.py`: JumpStart artifact + HF DLC image, `ml.p3.2xlarge`).
- `bots/` – Lex V2 bot import from `bots/bot_files/*.zip`; `cognito_stack/`, `apis/webhooks.py`, `s3_cloudfront/`.
- `front_end/` – CRA React app. `src/aws-exports.js` is gitignored and must be created from the README template.

## Commands
```bash
cd cool-image-bot
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
# the stack needs front_end/build before synth:
(cd front_end && npm install && DISABLE_ESLINT_PLUGIN=true npm run build)
cdk synth
cdk deploy        # real resources incl. a GPU SageMaker endpoint (cost!)
cdk destroy
```

## Dependencies
- `aws-cdk-lib==2.277.0`, `constructs>=10,<11`, CDK CLI 2.x, Node 18+ for the front end.
- Lambda runtime **Python 3.13**. `cool_image_hook` needs the Pillow layer + common layer; numpy is no longer used.

## Conventions / gotchas
- Rebuild `layers/pil.zip` with the documented method when changing runtime: `pip install pillow --platform manylinux2014_x86_64 --only-binary=:all: -t python/ && zip -r pil.zip python requirements.txt` (https://docs.aws.amazon.com/lambda/latest/dg/python-layers.html).
- `DISABLE_ESLINT_PLUGIN=true` is needed for `npm run build` with current Node (eslint-config-react-app 7.0.1 / eslint-plugin-jest 25 mismatch).
- `aws_cloudfront_origins.S3Origin` is deprecated in CDK (still works); migrating to `S3BucketOrigin` is a follow-up.
- Do not hardcode model/service identifiers without checking the official docs.

## Recent changes
- 2026-11: Lambda runtime `python3.8` -> `python3.13`; Pillow layer rebuilt for 3.13; removed the `AWSLambda-Python38-SciPy1x` managed numpy layer (3.8-only) by building the PNG with `Image.frombytes` (verified pixel-identical to the previous `fromarray` path); `aws-cdk-lib` 2.94.0 -> 2.277.0; README build-order note. Verified: `cdk synth` OK (3 functions on python3.13), handlers import under Python 3.13 with the new layer. Not deployed.
