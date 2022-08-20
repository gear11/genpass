# genpass
Python command-line client for generating domain-specific passwords using a secure hash of the domain
with a master password or passphrase.

### Background ###

I've used this kind of approach for years, wanting to have long, unguessable passwords but not wanting to use a
password manager due to a history of hacks (for example: https://www.tomsguide.com/news/password-manager-hacks).

About the only downside I've experienced is that the password for a site is deterministic, so if the site forces you to rotate
passwords (which NIST actually recommends against: https://www.auditboard.com/blog/nist-password-guidelines/)
then you need to get a bit hacky, for example by changing the length or using a different domain name
(for example, for `adp` I might instead use `pay` or for `fidelity` I might instead use `401k`)

### Key Attributes ###

- Generates a unique password for each domain from a single master password  / pass phrase.
- Never stores passwords or the passphrase. This is not only secure, but it also means you just need access to this
  script, vs. needing to plug into a cloud-based password manager on every device you use.
- Stores the options used to generate a password, so you don't have to remember them (see below).
- Passwords are a base64 encoded SHA-256 hash, so will likely contain upper / lower / digits automatically,
  but if you are unlucky and the generated password doesn't meet the site requirements, you can force additional requirements.
- If you want to reuse passwords for low-risk sites, can just use a generic word like `streaming` as the domain.

### Usage ###

    usage: genpass [-h] [-L LENGTH] [-d] [-s] [-u] [-l] domain
    
    Generate a password for the given domain
    
    positional arguments:
    domain      The domain for which to generate a password
    
    optional arguments:
    -h, --help  show this help message and exit
    -L LENGTH   Specify the length of the output password (default 12, specify 0
                for max length of ~40)
    -d          Require a digit in the output
    -s          Require a special character in the output
    -u          Require an upper case in the output
    -l          Require an lower case in the output

Example usage:

    % genpass google
    Passphrase: (type in a long, hard to guess passphrase, but can be the same for all domains)
    OzH91+Za8X3p

### Options (and storing them) ###

If a site has password requirements not satisfied by the default generated password, for example length longer or shorter than 12,
or needing a special character and the default does not include one, you can use options to force a digit, special,
upper, or lower in the output, or to set the length (specify 0 to yield the max length, which is about 40 characters).
Since it may be difficult to remember which options you used for which sites, the tool will create a `.genpass` file
that is populated with the options for a domain any time non-default options are used. So for example:

    % genpass -L 15 -s foo
    Passphrase:
    Saving prefs for foo to .genpass
    kixMgdyUYsyz-Gf

Now the next time you use genpass for `foo` you don't need to remeber the options:

    % genpass foo
    Passphrase:
    Loaded prefs for foo from .genpass: Requires(length=15, digit=False, special=True, upper=False, lower=False)
    kixMgdyUYsyz-Gf

The options are stored in the local file `.genpass` in JSON format. 

### Disclaimer ###

- Use this at your own risk. I have used this system for years and it has worked well for me but may not for you.
- If you do use this system, be very careful with your master passphrase. Make it long and unguessable and keep it secret.
- Always secure your important accounts with 2FA.
- I don't plan to do much maintenance here since this is a very stable approach but would consider any pull request that 
  preserves the Key Attributes above.