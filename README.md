# drone-ecs-plugin

### Usage

#### The plugin allows handling logs with `awslogs` log driver, as well as using secrets in the designated ECS environment
#### Note that the last two parameters do not have a value so that the plugin would search them in the secrets

```yaml
 deploy-production:
    image: omerxx/drone-ecs-plugin:17
    cluster: my-cluster
    region: us-east-1
    service: my-service
    family: my-service
    image_name: reg.company.com/image
    image_tag: ${DRONE_BUILD_NUMBER}
    environment_variables:
      - BRANCH=${DRONE_BRANCH}
      - SHA1=${DRONE_COMMIT_SHA}
      - BUILD_NUMBER=${DRONE_BUILD_NUMBER}
      - AWS_ACCESS_KEY_ID=
      - AWS_SECRET_ACCESS_KEY=
    port_mappings:
      - 0 3000
    memory: 800
    log_driver: awslogs
    log_options:
      - awslogs-group=my-service
      - awslogs-region=us-east-1
    secrets:
      - aws_access_key_id
      - aws_secret_access_key
    when:
      branch: [master]
```
