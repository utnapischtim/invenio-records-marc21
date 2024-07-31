// This file is part of Invenio.
//
// Copyright (C) 2021-2023 Graz University of Technology.
//
// Invenio-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import React from "react";
import ReactDOM from "react-dom";

import { getInputFromDOM } from "@js/invenio_rdm_records";
import { Marc21DepositForm } from "./Marc21DepositForm";

ReactDOM.render(
  <Marc21DepositForm
    record={getInputFromDOM("marc21-deposit-record")}
    preselectedCommunity={getInputFromDOM("marc21-deposit-draft-community")}
    files={getInputFromDOM("marc21-deposit-files")}
    config={getInputFromDOM("marc21-deposit-config")}
    templates={getInputFromDOM("marc21-deposit-templates")}
    permissions={getInputFromDOM("marc21-deposit-permissions")}
  />,
  document.getElementById("marc21-deposit-form")
);
