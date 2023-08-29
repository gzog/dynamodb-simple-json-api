module "dynamodb_table" {
  source   = "terraform-aws-modules/dynamodb-table/aws"

  name                        = "data"
  hash_key                    = "PK"
  range_key                   = "SK"
  table_class                 = "STANDARD"
  deletion_protection_enabled = true

  attributes = [
    {
      name = "PK"
      type = "S"
    },
    {
      name = "SK"
      type = "S"
    },
    {
      name = "VALUE"
      type = "S"
    }
  ]

  billing_mode                 = "PROVISIONED"

  read_capacity                = 25
  write_capacity               = 25
   
  tags = {
    Terraform   = "true"
    Environment = "production"
  }
}