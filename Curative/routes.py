import dataclasses
import os
import pprint as p

from flask import flash, render_template, redirect, url_for, session, request

from Curative import app, load_dotenv
from Curative.forms import LoginForm, ShippingAddressForm, SchedulePickupForm
from Curative.models import (
    ShipFromAddress,
    ShipToAddress,
    Package,
    PackageWeight,
    PackageDimensions,
    PickupObj,
    PickupContactDetails,
    PickupWindow
)
from Curative.se_client import ShipEngine

load_dotenv()


@app.route("/", methods=["GET", "POST"])
def index():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            session["user_key"] = form.password.data
            if form.password.data == os.getenv("SITE_PASSWORD"):
                flash("Success! - You are logged in.", "info")
                return redirect(url_for("curative_returns"))
            else:
                flash(
                        "Log in failed, please check password for typo's and retry.", "danger"
                )
    return render_template("login.html", title="Curative Login", form=form, session=session)


@app.route("/curative_returns", methods=["GET", "POST"])
def curative_returns():
    form = ShippingAddressForm()

    if form.is_submitted():
        if form.return_destination.data == "DC Lab":
            curative_ship_to = ShipToAddress(
                    name="Curative DC Lab",
                    phone="1-789-456-1234",
                    company_name="Curative",
                    address_line1="3330 New York Ave NE",
                    address_line2=None,
                    address_line3=None,
                    city_locality="Washington",
                    state_province="DC",
                    postal_code="20002",
                    country_code="US",
                    address_residential_indicator="no",
            )
        else:
            curative_ship_to = ShipToAddress(
                    name="Curative San Dimas Lab",
                    phone="1-789-456-1234",
                    company_name="Curative Inc.",
                    address_line1="430 South Cataract Ave",
                    address_line2=None,
                    address_line3=None,
                    city_locality="San Dimas",
                    state_province="CA",
                    postal_code="91773",
                    country_code="US",
                    address_residential_indicator="no",
            )

        user_ship_from = ShipFromAddress(
                name=form.name.data,
                phone=form.phone.data,
                company_name=form.company_name.data,
                address_line1=form.address_line_1.data,
                address_line2=form.address_line_2.data,
                address_line3=form.address_line_3.data,
                city_locality=form.city_locality.data,
                state_province=form.state_province.data,
                postal_code=form.postal_code.data,
                country_code=form.country_code.data,
                address_residential_indicator=form.address_residential_indicator.data,
        )

        weight = PackageWeight(
                value=2.5,
                unit="pound"
        )

        dims = PackageDimensions(
                unit="inch",
                length=12.5,
                width=12.5,
                height=12.5
        )

        package = Package(
                weight=dataclasses.asdict(weight),
                dimensions=dataclasses.asdict(dims)
        )

        se = ShipEngine()

        se_data = se.create_label(
                ship_to_address=curative_ship_to,
                ship_from_address=user_ship_from,
                packages=[package],
                label_message=form.number_of_tests_to_return.data
        )
        flash(f"Label Generated! - Print you return label below.", "primary")
        pickup_form = SchedulePickupForm()
        return render_template("return_label.html",
                               title="Print Return Label",
                               se_data=se_data, form=pickup_form)
    else:
        flash(f"Something went wrong:\n Please check your form inputs for errors and retry.", "danger")
    return render_template(
            "test_returns.html", title="Curative Test Returns", form=form
    )


@app.route("/logout")
def logout():
    session.pop("user_key", None)
    return redirect(url_for("index"))


@app.route("/pickup", methods=["POST"])
def return_label():
    form = SchedulePickupForm()

    pickup_window_data = PickupWindow(
            start_at='',
            end_at=''
    )

    pickup_contact_data = PickupContactDetails(
            name=form.contact_name.data,
            email=form.contact_email.data,
            phone=form.contact_phone.data
    )

    pickup_data = PickupObj(
            label_ids=[form.label_id.data],
            contact_details=dataclasses.asdict(pickup_contact_data),
            pickup_notes=form.pickup_notes.data,
            pickup_window=""
    )

    se = ShipEngine()

    req = {dataclasses.asdict(pickup_data)}
    return se.post("pickup", json=req)
