terraform {
  backend "gcs" {
    bucket = "chichavl-storage-bucket"
    prefix = "terraform/state"
  }
}
