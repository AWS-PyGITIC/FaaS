# How to Set up Terraform

To decouple the project and try to have as much as secure as possible the terraform.tfvars is not published into the git repo.


At this moment this file just defined the secrets of aws account.

So you need to create the `terraform.tfvars` file and set all the vars from the `variables.tf`

```
variable_name="value"
```