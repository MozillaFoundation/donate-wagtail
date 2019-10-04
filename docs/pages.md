# Pages

Content on this site is managed using the [Wagtail CMS](https://wagtail.io).
There are just two content types used.

## Landing page

The `LandingPage` content type is used for the root page of the site. It acts
as the home page, and provides a donation form for all non-specific donations.

The configurable content on this page is:

- Page title
- Introductory text
- Featured image that appears above introductory text

Additional settings on this page are:

- Meta title
- Meta description
- Campaign ID (used for associating donations with a campaign in Basket)
- Project (one of `mozillafoundation` or `thunderbird`, used for associating donations with a project in Basket)

## Campaign page

The `CampaignPage` content type can be created as a child of a `LandingPage`,
and is used to provide a customized, mission-specific donation page.

The configurable content on this page is:

- Page title
- Introductory text
- Hero image that appears behind the page title
- Featured image that appears above introductory text

In addition, the default suggested donation amounts for each currency can be
overridden for a campaign. For example, on Pi Day, you could specify an override
for the USD currency such that the suggested donation amounts for USD are $3.14,
$6.28 and $9.42.

Any currency for which overrides are not specified will fall back to the global
defaults. The number of suggested amounts is also flexible - 1 to 5 options are
allowed.

Additional settings on this page are:

- Meta title
- Meta description
- Campaign ID (used for associating donations with a campaign in Basket)
- Project (one of `mozillafoundation` or `thunderbird`, used for associating donations with a project in Basket)
