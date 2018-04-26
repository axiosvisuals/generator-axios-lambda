package utils

import (
	"log"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/awserr"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/secretsmanager"
)

// GetSecrets : Gets secrets from AWS secrets manager given their id. Returns a struct of secrets
// The AWS Region needs to be provided in the AWS shared config or on the
// environment variable as `AWS_REGION`. Credentials also must be provided
// Will default to shared config file, but can load from environment if provided.
func GetSecrets(id string) (secrets *secretsmanager.GetSecretValueOutput, err error) {
	// All clients require a Session. The Session provides the client with
	// shared configuration such as region, endpoint, and credentials. A
	// Session should be shared where possible to take advantage of
	// configuration and credential caching. See the session package for
	// more information.
	sess := session.Must(session.NewSession())

	// Create a new instance of the service's client with a Session.
	// Optional aws.Config values can also be provided as variadic arguments
	// to the New function. This option allows you to provide service
	// specific configuration.
	svc := secretsmanager.New(sess)

	input := &secretsmanager.GetSecretValueInput{SecretId: aws.String(id)}

	result, err := svc.GetSecretValue(input)
	if err != nil {
		if aerr, ok := err.(awserr.Error); ok {
			switch aerr.Code() {
			case secretsmanager.ErrCodeResourceNotFoundException:
				log.Fatal(secretsmanager.ErrCodeResourceNotFoundException, aerr.Error())
			case secretsmanager.ErrCodeInvalidParameterException:
				log.Fatal(secretsmanager.ErrCodeInvalidParameterException, aerr.Error())
			case secretsmanager.ErrCodeInvalidRequestException:
				log.Fatal(secretsmanager.ErrCodeInvalidRequestException, aerr.Error())
			case secretsmanager.ErrCodeDecryptionFailure:
				log.Fatal(secretsmanager.ErrCodeDecryptionFailure, aerr.Error())
			case secretsmanager.ErrCodeInternalServiceError:
				log.Fatal(secretsmanager.ErrCodeInternalServiceError, aerr.Error())
			default:
				log.Fatal(aerr.Error())
			}
		} else {
			// Print the error, cast err to awserr.Error to get the Code and
			// Message from an error.
			log.Fatal(err.Error())
		}
		return nil, err
	}

	return result, err
}
