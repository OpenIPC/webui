![OpenIPC Logo](https://cdn.themactep.com/images/logo_openipc.png)

microbe-web
===========

Microbe Web UI is a default web interface for [OpenIPC firmware][openipcfw].

Microbe Web is lightweight but powerful interface written mostly in shell
and [haserl][haserl]. Web UI listens on port 85.

### Muliti-language UI and Translation

To change the Web Interface language, please select Settings -> Web UI Settings
from the top menu, and then select your desired language from the dropdown list
in the form. Submit the form to save apply changes.

To add a missing language translation, please take a look at shell files in
`/files/www/cgi-bin/locale/` directory. You might want to use `en.sh` file as a
template. It contains all the variables you need to assign proper values to.
Make a copy of that file, give the copy a name according to [ISO 639-1][iso639].

Language file is a shell script that starts with a shebang and followed by the
name of the language as a comment:
```
#!/bin/sh
#name:Klingonese
```

Below that header goes a list of variables and their values that constitute the
new language support. Update the values, test the new locale, then create a pull
request.

More documentation is available [in our wiki][wiki].

### Support

OpenIPC offers two levels of support.

- Free support through the community via [chat][telegram] and
  [mailing lists][maillist].
- Paid commercial support directly from the team of developers.

Please consider subscribing for paid commercial support if you intend to use our
product for business. As a paid customer, you will get technical support and
maintenance services directly from our skilled team. Your bug reports and
feature requests will get prioritized attention and expedited solutions. It's a
win-win strategy for both parties, that would contribute to the stability your
business, and help core developers to work on the project full-time.

If you have any specific questions concerning our project, feel free to
[contact us](mailto:flyrouter@gmail.com).

### Participating and Contribution

If you like what we do, and willing to intensify the development, please
consider participating.

You can improve existing code and send us patches. You can add new features
missing from our code.

You can help us to write a better documentation, proofread and correct our
websites.

You can just donate some money to cover the cost of development and long-term
maintaining of what we believe is going to be the most stable, flexible, and
open IP Network Camera Framework for users like yourself.

You can make a financial contribution to the project at [Open Collective][oc].

Thank you.

<p align="center">
<a href="https://opencollective.com/openipc/contribute/backer-14335/checkout" target="_blank"><img src="https://opencollective.com/webpack/donate/button@2x.png?color=blue" width="375" alt="Open Collective donate button"></a>
</p>

[openipcfw]: https://github.com/OpenIPC/firmware
[haserl]: http://haserl.sourceforge.net/
[iso639]: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
[wiki]: https://github.com/OpenIPC/firmware/wiki/microbe-web
[telegram]: https://openipc.org/#telegram-chat-groups
[maillist]: https://github.com/OpenIPC/firmware/discussions
[oc]: https://opencollective.com/openipc/contribute/backer-14335/checkout
[pp]: https://www.paypal.com/donate/?hosted_button_id=C6F7UJLA58MBS
[ym]: https://openipc.org/donation/yoomoney.html
