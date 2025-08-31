export type EmailType = {
  sender: string,
  message: string,
  classification: string,
  suggestion: string
}

export type PreferenceType = {
  sender: string,
  password: string
}

export type SendEmailType = {
  recipient: string,
  sender: string,
  password: string,
  message: string
}