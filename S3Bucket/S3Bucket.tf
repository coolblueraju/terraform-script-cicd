resource "aws_s3_bucket" "b" {
  bucket = var.bucket_name

  tags = {
    Name        = "CloudQuixLabs"
    Environment = "Testing"
  }
}